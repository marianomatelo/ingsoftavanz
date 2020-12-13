from django.db import models


class User(models.Model):
    rol = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=50)
    key = models.CharField(max_length=100)