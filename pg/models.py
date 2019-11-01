from django.db import models


class User(models.Model):
    rol = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=50)


# class Dataset_Meta(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=300)
#     problem = models.CharField(max_length=20)
#     frequency = models.CharField(max_length=30)
#     user = models.CharField(max_length=100)
#     last_mod = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.dataset