from djoser.serializers import UserCreateSerializer
from .models import Usuario

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Usuario
        fields = ('id', 'username', 'password', 'empresa')