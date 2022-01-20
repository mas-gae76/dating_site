from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import *
from PIL import Image
from django.conf import settings
from django_filters import rest_framework as filters


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'М', 'Мужской'
        FEMALE = 'Ж', 'Женский'
        __empty__ = 'Укажите Ваш пол'

    avatar = models.ImageField(verbose_name='Аватар', default=None, upload_to=get_timestamp_path_user)
    gender = models.CharField(max_length=1, verbose_name='Пол', choices=Gender.choices, default=Gender.MALE)
    first_name = models.CharField(verbose_name='Имя', max_length=40)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    email = models.EmailField(max_length=128, unique=True)
    username = models.CharField(blank=True, max_length=10)
    latitude = models.DecimalField(verbose_name='Широта', max_digits=6, decimal_places=2)
    longitude = models.DecimalField(verbose_name='Долгота', max_digits=6, decimal_places=2)
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super().save()
        if self.avatar:
            avatar = Image.open(self.avatar.path)
            watermark = Image.open(settings.WATERMARK_PATH)
            watermark.thumbnail((250, 250))
            x = avatar.size[0] - watermark.size[0] - 20
            y = avatar.size[1] - watermark.size[1] - 20
            avatar.paste(watermark, (x, y))
            avatar.save(self.avatar.path)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Sympathy(models.Model):
    who = models.ForeignKey(User, on_delete=models.CASCADE, related_name='who')
    whom = models.ForeignKey(User, verbose_name='Кого хотите оценить?', on_delete=models.CASCADE, related_name='whom')
    matching = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.who} оценил {self.whom}'

    class Meta:
        verbose_name = 'Взаимная симпатия'
        verbose_name_plural = 'Взаимные симпатии'
        constraints = [models.UniqueConstraint(fields=('who', 'whom'), name='unique_matching')]


class UserFilter(filters.FilterSet):
    first_name = filters.CharFilter(label='Имя', lookup_expr='icontains')
    last_name = filters.CharFilter(label='Фамилия', lookup_expr='icontains')
    gender = filters.CharFilter(label='Пол', lookup_expr='icontains')
    distance = filters.NumberFilter(label='Дистанция')

    class Meta:
        models = User
        fields = ('first_name', 'last_name', 'gender', 'distance')
