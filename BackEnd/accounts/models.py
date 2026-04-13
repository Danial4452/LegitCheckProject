from django.db import models
from django.contrib.auth.hashers import make_password


class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class User(models.Model):
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.login

    def set_password(self, raw_password):
        self.password = make_password(raw_password)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.login

