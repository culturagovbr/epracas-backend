from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    praca_manager = serializers.URLField(
        source='is_praca_manager', read_only=True)

    class Meta:
        model = User
        exclude = ('password', )
