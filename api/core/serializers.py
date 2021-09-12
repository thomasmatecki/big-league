"""
Core serializers
"""
from collections import OrderedDict

from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sessions.models import Session
from django.middleware.csrf import CSRF_SESSION_KEY
from rest_framework import serializers
from rest_framework.utils import model_meta


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
    username = serializers.CharField(source="user.username")
    password = serializers.CharField(write_only=True)
    csrf_token = serializers.SerializerMethodField(read_only=True)
    expiry_date = serializers.DateTimeField(
        source="session.get_expiry_date", read_only=True
    )

    def create(self, _validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        request = instance
        form_data = {
            "username": validated_data["user"]["username"],
            "password": validated_data["password"],
        }
        form = AuthenticationForm(request=request, data=form_data)
        if form.is_valid():
            auth.login(request, form.get_user())
            return request
        raise serializers.ValidationError(form.errors)

    def get_csrf_token(self, instance):
        return instance.session.get(CSRF_SESSION_KEY)

    class Meta:
        model = Session
        fields = ["username", "password"]


class HyperLinkedObjectSerializer(serializers.HyperlinkedModelSerializer):
    # TODO this should be a field
    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.url_field_name = "url"
        self.sources = kwargs.pop("sources", {})
        super().__init__(*args, **kwargs)

    def get_field_names(self, *_args):
        return ["id", "url", "name"]

    def get_uniqueness_extra_kwargs(self, field_names, declared_fields, extra_kwargs):
        return {}, {}

    def get_fields(self):

        info = model_meta.get_field_info(self.model)

        field_names = self.get_field_names([], info)
        extra_kwargs = self.get_extra_kwargs()
        extra_kwargs, hidden_fields = self.get_uniqueness_extra_kwargs(
            field_names, [], extra_kwargs
        )

        fields = OrderedDict()

        for field_name in field_names:

            extra_field_kwargs = extra_kwargs.get(field_name, {})
            source = extra_field_kwargs.get("source", self.sources.get(field_name, "*"))
            if source == "*":
                source = field_name

            # Determine the serializer field class and keyword arguments.
            field_class, field_kwargs = self.build_field(source, info, self.model, None)

            field_kwargs = self.include_extra_kwargs(field_kwargs, extra_field_kwargs)
            if source != field_name:
                field_kwargs["source"] = source

            fields[field_name] = field_class(**field_kwargs)

        fields.update(hidden_fields)

        return fields

    def get_validators(self):
        return []

    class Meta:
        pass
