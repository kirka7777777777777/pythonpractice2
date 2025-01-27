import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.conf import settings


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"



class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name





class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнена'),
    ]
    CATEGORY_CHOICES = [  # Определите список категорий как кортеж кортежей
        ('3d_design', '3D-дизайн'),
        # Используйте значения, подходящие для хранения в базе данных (без пробелов, строчные буквы)
        ('2d_design', '2D-дизайн'),
        ('sketch', 'Эскиз'),
        ('other', 'Другое'),  # Добавьте свои категории
    ]  # Ваши категории (как кортеж кортежей)

    title = models.CharField(max_length=255, verbose_name="Название заявки")
    description = models.TextField(verbose_name="Описание заявки")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    photo = models.ImageField(upload_to='application_photos/', blank=True, null=True, verbose_name="Фото помещения или план") # blank=True, null=True для необязательного фото при создании
    design = models.ImageField(upload_to='design_photos/', blank=True, null=True, verbose_name="Дизайн (для статуса 'Выполнена')") # Поле для загрузки дизайна
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Временная метка")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус заявки")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    comment = models.TextField(blank=True, verbose_name="Комментарий администратора") # Комментарий для статуса "Принято в работу"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-timestamp']

    def __str__(self):
        return self.title



class ImageUpload(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')  # Папка внутри MEDIA_ROOT

    def __str__(self):
        return self.title