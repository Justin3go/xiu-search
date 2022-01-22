from djoser.serializers import UserCreateSerializer,UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "username", "password")
        
class MyUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "avator")