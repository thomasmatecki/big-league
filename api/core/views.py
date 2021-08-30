from api.core.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.viewsets import ReadOnlyModelViewSet


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
