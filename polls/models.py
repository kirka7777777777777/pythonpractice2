import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

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
    categories = models.ManyToManyField('CategoryForm', blank=True, related_name='user_profiles')

    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"


class CategoryForm(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    class Meta:
            verbose_name = "Категория"
            verbose_name_plural = "Категории"
            ordering = ['name']

    def __str__(self):
            return self.name




class ImageUpload(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')  # Папка внутри MEDIA_ROOT

    def __str__(self):
        return self.title