from users.managers import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import UserQuerySet

class User(AbstractUser):

    email_verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='О себе')
    
    job = models.CharField(max_length=50, verbose_name='Текущая работа', default='Не указана', blank=True, null=True)
    rank_score = models.FloatField(default=0)
    objects = CustomUserManager()

    avatar = models.ImageField(upload_to='user_avatar', blank=True, null=True, verbose_name='Аватар')
    
    def __str__(self):
        return self.username

class EmailVerification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="email_verifications"
    )

    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

class PasswordReset(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_resets",
    )

    code = models.CharField(
        max_length=6,
    )

    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]