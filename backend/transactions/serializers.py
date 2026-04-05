from rest_framework import serializers
from .models import Transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import re

class TransactionSerializer(serializers.ModelSerializer):
    # Return dates in day, month (abbreviation), year format
    date = serializers.DateField(format="%d-%b-%Y")

    class Meta:
        model = Transaction
        fields = ["id", "amount", "category", "date", "description"]

class RegisterSerializer(serializers.ModelSerializer):
    # Make sure the password never gets sent to the browser
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain a capital letter.")
        if not re.search(r'[0-9]', value):
            raise ValidationError("Password must contain a number.")
        if not re.search(r'[!@#$%^&*]', value):
            raise ValidationError("Password must contain a special character.")
            
        return value
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
