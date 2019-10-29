from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=50)


class Dataset_Meta(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    problem = models.CharField(max_length=20)
    frequency = models.CharField(max_length=30)
    user = models.CharField(max_length=100)
    last_mod = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.dataset


class Daemon(models.Model):
    dataset_id = models.IntegerField()
    name = models.CharField(max_length=100)
    dataset_description = models.CharField(max_length=300)
    run_description = models.CharField(max_length=300)
    problem = models.CharField(max_length=20)
    frequency = models.CharField(max_length=30)
    user = models.CharField(max_length=100)
    sent_date = models.DateTimeField(auto_now_add=True)
    run_date = models.DateTimeField(default=None, blank=True, null=True)
    status = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    clean = models.CharField(max_length=50)
    scaling = models.CharField(max_length=50)
    training = models.CharField(max_length=50)
    params = models.CharField(max_length=500, default=None, blank=True, null=True)

    def __str__(self):
        return self.id