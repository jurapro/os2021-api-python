from rest_framework import serializers
from rest_framework.fields import CharField

from .models import User, Role


class LoginSerializer(serializers.ModelSerializer):
    login = CharField(required=True)
    password = CharField(required=True)

    class Meta:
        model = User
        fields = ['login', 'password']


class UserListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        return {
            'data': super().to_representation(data)
        }

    @property
    def data(self):
        ret = serializers.BaseSerializer.data.fget(self)
        return serializers.ReturnDict(ret, serializer=self)


class UserSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source='role.name')

    class Meta:
        model = User
        list_serializer_class = UserListSerializer
        fields = ['id', 'name', 'login', 'status', 'group']


class UserCreateSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Role.objects.all()
    )

    def create(self, validated_data):
        role_id = validated_data['role_id'].id
        validated_data['role_id'] = role_id
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        exclude = ['role']
