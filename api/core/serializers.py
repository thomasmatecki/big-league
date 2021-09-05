"""
Core serializers
"""
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sessions.models import Session
from rest_framework import exceptions, serializers


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


class SessionSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    expiry_date = serializers.DateTimeField(source="get_expiry_date", read_only=True)

    def get_object(self):
        pass

    def create(self, validated_data):
        request = self.context["request"]
        form = AuthenticationForm(request=request, data=validated_data)
        if form.is_valid():
            auth.login(request, form.get_user())
            return request.session
        raise serializers.ValidationError(form.errors)

    class Meta:
        model = Session
        fields = ["username", "password"]
