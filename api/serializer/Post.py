from rest_framework import serializers

from fr_sys.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'uuid',
            'body',
            'created_at',
            'post_by',
            'post_by_fed'
        )
