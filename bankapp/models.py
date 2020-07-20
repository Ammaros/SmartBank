from django.db import models
from django.contrib.auth.forms import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    balance = models.IntegerField()

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    Amount = models.IntegerField()