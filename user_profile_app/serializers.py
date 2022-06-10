from rest_framework.serializers import *
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TokenSerializer(ModelSerializer):
    user = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Token
        fields = ['user', 'session_token']
        depth = 1
