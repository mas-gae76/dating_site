from django.db import models
from django.contrib.auth.models import AbstractUser
from utils import *
from imagekit import ImageSpec


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'М', 'Мужской'
        FEMALE = 'Ж', 'Женский'
        __empty__ = 'Укажите Ваш пол'
    avatar = models.ImageField(verbose_name='Аватар', blank=True, upload_to=get_timestamp_path_user)
    gender = models.CharField(verbose_name='Пол', choices=Gender.choices, default=Gender.MALE)
    name = models.CharField(verbose_name='Имя', max_length=40)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.name} {self.last_name}'

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
