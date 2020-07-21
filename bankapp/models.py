from django.db import models
from django.contrib.auth.forms import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    balance = models.IntegerField()
    transactions = models.IntegerField(null=False, blank=True, default=0)
    balanceSpent = models.IntegerField(null=False, blank=True, default=0)

    def __str__(self):
        return self.user.username
