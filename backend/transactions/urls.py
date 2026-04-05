from django.urls import path
from .views import (RegisterView,
                    LoginView,
                    LogoutView, 
                    UploadCSV, 
                    SpendingByCategory, 
                    SpendingByMonth, 
                    SpendingByDay, 
                    TransactionHistory,
                    TransactionDetail,
                    get_csrf_token)

urlpatterns = [
    path('csrf/', get_csrf_token),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upload/', UploadCSV.as_view(), name='upload-csv'),
    path('category/', SpendingByCategory.as_view(), name='category'),
    path('monthly/', SpendingByMonth.as_view(), name='monthly'),
    path('daily/', SpendingByDay.as_view(), name='daily'),
    path('history/', TransactionHistory.as_view(), name='transaction-history'),
    path('transactions/<int:transaction_id>/', TransactionDetail.as_view(), name='transaction'),

]