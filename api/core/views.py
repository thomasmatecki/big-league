from api.core import serializers
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from rest_framework import mixins, viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class SessionViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = []
    authentication_classes = []
    queryset = Session.objects.all()
    serializer_class = serializers.SessionSerializer
