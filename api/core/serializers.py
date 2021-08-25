"""
Core serializers
"""
from rest_framework import serializers
from django.contrib import auth


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth.get_user_model()
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "is_staff",
            "is_superuser",
            "is_active",
        ]
