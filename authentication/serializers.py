from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', )

# class UserSerializer(serializers.Serializer):
#     id_pub = serializers.UUIDField(read_only=True)
#     email = serializers.EmailField()
#     email_verified = serializers.BooleanField()
#     family_name = serializers.CharField()
#     first_name = serializers.CharField()
#     full_name = serializers.CharField()
#     given_name = serializers.CharField()
#     name = serializers.CharField()
#     picture = serializers.URLField()
#     profile_picture_url = serializers.URLField()
#     surname = serializers.CharField()
#     is_staff = serializers.BooleanField()

#     def update(self, instance, validated_data):
#         instance.email_verified = validated_data.get(
#             'email_verified',
#             instance.email_verified)
#         instance.email = validated_data.get(
#             'email',
#             instance.email)
#         instance.family_name = validated_data.get(
#             'family_name',
#             instance.family_name)
#         instance.first_name = validated_data.get(
#             'first_name',
#             instance.first_name)
#         instance.full_name = validated_data.get(
#             'full_name',
#             instance.first_name)
#         instance.given_name = validated_data.get(
#             'full_name',
#             instance.given_name)
#         instance.name = validated_data.get(
#             'name',
#             instance.name)
#         instance.picture = validated_data.get(
#             'picture',
#             instance.picture)
#         instance.profile_picture_url = validated_data.get(
#             'profile_picture_url',
#             instance.profile_picture_url)
#         instance.surname = validated_data.get(
#             'surname',
#             instance.surname)
#         instance.is_staff = validated_data.get(
#             'is_staff',
#             instance.is_staff)

#         instance.save()
#         return instance
