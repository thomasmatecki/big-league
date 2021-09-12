from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from rest_framework import mixins, viewsets

from api.core import serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class SessionViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = []
    queryset = Session.objects.all()
    serializer_class = serializers.SessionSerializer

    def get_object(self):
        return self.request

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if redirect_to := request.query_params.get("next"):
            response.status_code = 303
            response.headers["Location"] = redirect_to
        return response
