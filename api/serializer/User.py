from rest_framework import serializers

from fr_sys.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'uuid',
            'username',
            'display_name',
            'description',
            'is_active',
            'is_bot',
            'is_manualFollow',
            'moderator',
            'administrator',
            'registered',
            'updated'
        )
