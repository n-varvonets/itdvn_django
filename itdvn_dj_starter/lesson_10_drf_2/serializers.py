from rest_framework import serializers
from django.contrib.auth.models import User
from lesson_8.models import GamerModel, GameModel


class GameModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameModel
        fields = '__all__'


class GamerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamerModel
        fields = ['nickname', 'email']


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер, который создает учетную запись
    Модель User и таблица в бд auth_user
    """
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}  # роль можно только записать при создании и в обмене мы дадим \
        # ему токен. Никак прочитать мы его не сможем.

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
