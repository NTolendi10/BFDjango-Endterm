from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
import os
from .Gender import gender
# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, is_seller=False, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, is_seller=is_seller, **extra_fields)
        user.set_password(password)
        user.save()
        # Profile.objects.create(user=user)
        return user

    def create_user(self, username, email=None, password=None, is_seller=False,
                    shopName="", shopEmail="",
                    **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, is_seller=False, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    gender = models.PositiveSmallIntegerField(choices=gender, default=0)
    cardDetails = models.CharField(max_length=100, blank=True, default="")
    age = models.IntegerField(default=0, blank=True)
    is_seller = models.BooleanField(default=False)
    location = models.CharField(max_length=150)

    users = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username', ]

    def __str__(self):
        return f"User : {self.username}"


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    shop = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=150)
    phoneNumber = models.CharField(max_length=150)

    def __str__(self):
        return f"Seller : {self.shop}"

    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'
        ordering = ['shop']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    products = models.ManyToManyField("api.Gadget", blank=True)
    picture = models.ImageField(upload_to='profile', default='nopic.png')

    def __str__(self):
        return f"Profile: {self.user.username}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
