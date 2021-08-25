from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth.models import User

from api.core.serializers import UserSerializer

class UserViewSet(ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()


    serializer_class = UserSerializer
