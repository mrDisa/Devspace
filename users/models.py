from users.managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserQuerySet

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='О себе')
    
    job = models.CharField(max_length=50, verbose_name='Текущая работа', default='Не указана', blank=True, null=True)
    rank_score = models.FloatField(default=0)
    objects = CustomUserManager()

    avatar = models.ImageField(upload_to='user_avatar', blank=True, null=True, verbose_name='Аватар')
    
    def __str__(self):
        return self.username