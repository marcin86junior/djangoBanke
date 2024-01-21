from .models import Account, Transaction
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "first_name", "last_name")
        write_only_fields = ("password",)
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        Account.objects.create(user=user, balance=0)
        return user


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "user"]


class MyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "account_no", "user", "balance"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "account", "amount", "transaction_type", "timestamp"]

    def __init__(self, *args, **kwargs):
        # Get the user from the context, which is set in the view
        user = kwargs.pop("user", None)
        super(TransactionSerializer, self).__init__(*args, **kwargs)

        # Filter the queryset for the account field to include only the user's account
        if user and user.is_authenticated:
            self.fields["account"].queryset = Account.objects.filter(user=user)
