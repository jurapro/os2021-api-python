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
        iterable = data.all() if isinstance(data, User) else data
        res = [self.child.to_representation(item) for item in iterable]
        return {'data': res}

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
        queryset=Role.objects.all(),
    )

    def validate_login(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Короткий логин")
        return value

    class Meta:
        model = User
        exclude = ['role']

