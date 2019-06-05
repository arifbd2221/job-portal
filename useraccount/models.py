from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class User(AbstractUser):
    username = None
    role = models.CharField(max_length=12, error_messages={
        'required': "Role must be provided"
    })

    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    gender_list = (('male', 'Male'), ('female', 'Female'),)
    gender = models.CharField(max_length=10, choices=gender_list, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __unicode__(self):
        return self.email
    
    objects = UserManager()