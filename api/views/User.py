from rest_framework import viewsets, mixins

from fr_sys.models import User

from api.serializer import UserSerializer


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    User viewset
    """
    queryset = User.objects.all().filter(is_suspend=False, is_active=True)
    serializer_class = UserSerializer
    lookup_field = "username"
