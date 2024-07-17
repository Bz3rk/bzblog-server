from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Topic(models.Model):
    name = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name
    
class Blog(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null = True)
    author = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ['-id']  

    def __str__(self):
        return self.body[0:10]
        