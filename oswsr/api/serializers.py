from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import CharField

from .models import User, Role, WorkShift, ShiftWorker


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


class WorkShiftSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=['%Y-%m-%d %H:%M'])
    end = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=['%Y-%m-%d %H:%M'])

    def validate_start(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('The start date of the shift cannot be earlier than now')
        return value

    def validate(self, data):
        if data['start'] >= data['end']:
            raise serializers.ValidationError('The end date of the shift cannot be earlier than the start date')
        return data

    class Meta:
        model = WorkShift
        exclude = ['active']


class WorkSiftDetailSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    end = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def to_representation(self, instance):
        return {
            'data': super().to_representation(instance)
        }

    class Meta:
        model = WorkShift
        fields = '__all__'


class ShiftWorkerSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = ShiftWorker
        exclude = ['user', 'work_shift']
