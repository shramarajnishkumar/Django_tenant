from django.db import models
from django.contrib.auth.models import AbstractUser
from authapp.models import Company

class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company', null=True)
    email = models.EmailField(null=True)
