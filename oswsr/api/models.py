from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.authentication import get_authorization_header

from .utilities import get_name_file


class Role(models.Model):
    name = models.CharField(max_length=100, blank=False)
    code = models.CharField(max_length=50, blank=False)

    class Meta:
        db_table = 'roles'


class User(AbstractBaseUser):
    name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    patronymic = models.CharField(max_length=100, blank=True)
    login = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=254, blank=False)
    photo_file = models.ImageField(max_length=254, upload_to=get_name_file, blank=True, null=True)
    api_token = models.CharField(max_length=254, blank=True)
    status = models.CharField(max_length=254, choices=[('working', 'working'), ('fired', 'fired')], default='working')
    last_login = models.DateTimeField(db_column='updated_at', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    USERNAME_FIELD = 'login'
    objects = BaseUserManager()

    @classmethod
    def get_auth_user(cls, request=None):
        keyword = 'Bearer'
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != keyword.lower().encode() or not auth[1]:
            return None
        return cls.objects.filter(api_token=auth[1].decode()).first()

    class Meta:
        db_table = 'users'
