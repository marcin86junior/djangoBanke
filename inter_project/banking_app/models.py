from django.db import models
from django.contrib.auth.models import User
import random


class Account(models.Model):
    def generate_random_account_no():
        return random.randint(10**11, 10**12 - 1)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_no = models.PositiveIntegerField(unique=True, default=generate_random_account_no)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #currency (to be added)

    def __str__(self):
        return str("User: ")+str(self.user)+str(", Account numer: ")+str(self.account_no)


class Transaction(models.Model):
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawl'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    # balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12) (to be added)
