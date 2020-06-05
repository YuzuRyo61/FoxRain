from rest_framework import viewsets

from fr_sys.models import Post

from api.serializer import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    Post ViewSet
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "uuid"
