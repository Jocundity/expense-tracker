from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from .models import Transaction
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from .serializers import TransactionSerializer, RegisterSerializer

import pandas as pd

# Create your views here.
@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF cookie set"})

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({"message": "User created and logged in"}, status=201)
        
        return Response(serializer.errors, status=400)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Incorrect username or password"}, status=401)
        
        login(request, user)

        return Response({"message": "Logged in"})
    
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})

class UploadCSV(View):

    def options(self, request, *args, **kwargs):
        return JsonResponse({"message": "OK"})

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Not authenticated"}, status=401)

        file = request.FILES.get('file')

        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        try:
            df = pd.read_csv(file)
            df["date"] = pd.to_datetime(df["date"])

            # Get user
            user = request.user

            # Delete old transaction data when a new csv is uploaded
            Transaction.objects.filter(user=user).delete()

            for i in range(len(df)):
                # Read row contents
                row = df.iloc[i]

                # Create transaction
                Transaction.objects.create(
                    user=user,
                    amount=row["amount"],
                    category=row["category"],
                    date=row["date"],
                    description=row["description"]
                )

            return JsonResponse({"message": "All rows saved to database"})
        except Exception as e:
            print(f"Upload error: {e}")
            return JsonResponse({"error": str(e)}, status=400)
    
class SpendingByCategory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = (
            Transaction.objects.filter(user=request.user)
            .values('category')
            .annotate(total=Sum('amount'))
        )

        # Make sure the total always prints with two decimal places
        for item in data:
            item["total"] = "{:.2f}".format(item["total"])

        return Response(data)
    
class SpendingByMonth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = (
            Transaction.objects.filter(user=request.user)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        # Make sure the total always prints with two decimal places
        for item in data:
            item["total"] = "{:.2f}".format(item["total"])

        return Response(data)
    
class SpendingByDay(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = (
            Transaction.objects.filter(user=request.user)
            .values('date')
            .annotate(total=Sum('amount'))
            .order_by('date')
        )

         # Make sure the total always prints with two decimal places
        for item in data:
            item["total"] = "{:.2f}".format(item["total"])

        return Response(data)

class TransactionHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = (
            Transaction.objects.filter(user=request.user)
            .order_by("-date")
            )
        
        serializer = TransactionSerializer(queryset, many=True)

        return Response(serializer.data)
    
class TransactionDetail(APIView):
    permission_classes = [IsAuthenticated]

    # Get single transaction
    def get_object(self, transaction_id, user):
        try:
            return Transaction.objects.get(id=transaction_id, user=user)
        except Transaction.DoesNotExist:
            return None
        except Exception as e: # debug
            print(f"Error in get_object: {e}")
            return None

        
    # Delete transaction
    def delete(self, request, transaction_id):
        transaction = self.get_object(transaction_id, user=request.user)

        if not transaction:
            return Response({"error": "Transaction not found"}, status=404)
        
        transaction.delete()
        return Response({"message": "Transaction deleted"}, status=200)

    # Update transaction
    def put(self, request, transaction_id):
        transaction = self.get_object(transaction_id, user=request.user)

        if not transaction:
            return Response({"error": "Transaction not found"}, status=404)
        
        serializer = TransactionSerializer(transaction, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
