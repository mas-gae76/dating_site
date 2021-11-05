from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=40, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.TextField(verbose_name='Название')
    image = models.URLField(verbose_name='Ссылка на картинку')
    price = models.PositiveIntegerField(verbose_name='Цена', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

