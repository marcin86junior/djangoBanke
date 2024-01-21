from .models import Account, Transaction, User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import (
    AccountSerializer,
    TransactionSerializer,
    UserSerializer,
    MyAccountSerializer,
)
import decimal


def homepage(request):
    return render(
        request,
        "banking_app/index.html",
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializer

    @action(detail=False, methods=["get"])
    def register_form(self, request):
        return render(request, "banking_app/user_registration.html")

    @action(detail=False, methods=["post"])
    def register(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if username and password:
            user = User.objects.create_user(
                username=username, password=password, email=email
            )
            login(request, user)
            return Response({"message": "Registration successful"})
        else:
            return Response({"error": "Username and password are required"})

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful"})
        else:
            return Response({"error": "Invalid credentials"})

    @action(detail=False, methods=["get"])
    def logout(self, request):
        logout(request)
        return Response({"message": "Logout successful"})

    @action(detail=False, methods=["get"])
    def current_user(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        else:
            return Response({"error": "Not logged in"})


class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def deposit(self, request, pk=None):
        account = self.get_object()
        amount = request.data.get("amount")
        account.balance += amount
        account.save()
        Transaction.objects.create(
            account=account, amount=amount, transaction_type="DEPOSIT"
        )
        return Response({"message": "Deposit successful"})

    @action(detail=True, methods=["post"])
    def withdraw(self, request, pk=None):
        account = self.get_object()
        amount = request.data.get("amount")
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            Transaction.objects.create(
                account=account, amount=amount, transaction_type="WITHDRAW"
            )
            return Response({"message": "Withdrawal successful"})
        else:
            return Response({"error": "Insufficient funds"})


class MyAccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    serializer_class = MyAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        accounts = self.get_queryset()
        return render(
            request, "banking_app/my_account_list.html", {"accounts": accounts}
        )


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.none()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        # Pass the user to the serializer during instantiation
        kwargs["user"] = self.request.user
        return super(TransactionViewSet, self).get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        transaction_type = serializer.validated_data["transaction_type"]
        amount = abs(serializer.validated_data["amount"])
        print(transaction_type)
        if transaction_type == "DEPOSIT":
            self.request.user.account.balance += amount
        elif transaction_type == "WITHDRAWAL":
            self.request.user.account.balance -= amount
        self.request.user.account.save()
        serializer.save(account=self.request.user.account)
        return Response(
            {"message": "Deposit successful"}, status=status.HTTP_201_CREATED
        )

    def create_deposit(self, request):
        amount = request.data.get("amount")
        serializer = self.get_serializer(
            data={"amount": amount, "transaction_type": "DEPOSIT"}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(account=self.request.user.account)
        return Response(
            {"message": "Deposit successful"}, status=status.HTTP_201_CREATED
        )

    def create_withdrawal(self, request):
        amount = request.data.get("amount")
        account = self.request.user.account

        if account.balance >= amount:
            serializer = self.get_serializer(
                data={"amount": amount, "transaction_type": "WITHDRAW"}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"message": "Withdrawal successful"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST
            )


class TransactionListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(account=self.request.user.account)

    def list(self, request, *args, **kwargs):
        transactions = self.get_queryset()
        return render(
            request, "banking_app/transaction_list.html", {"transactions": transactions}
        )


class TransferView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "banking_app/transfer_form.html")

    def post(self, request, *args, **kwargs):
        from_account_id = request.data.get("from_account_id")
        to_account_id = request.data.get("to_account_id")
        amount = request.data.get("amount")

        try:
            from_account = Account.objects.get(
                account_no=from_account_id, user=request.user
            )
            to_account = Account.objects.get(account_no=to_account_id)

            if decimal.Decimal(from_account.balance) >= decimal.Decimal(amount):
                # Deduct the amount from the logged user account
                from_account.balance -= decimal.Decimal(amount)
                from_account.save()

                # Add the amount to the destination account
                to_account.balance += decimal.Decimal(amount)
                to_account.save()

                # Create a transaction record
                Transaction.objects.create(
                    account=from_account,
                    amount=decimal.Decimal(amount),
                    transaction_type="TRANSFER_OUT",
                )

                Transaction.objects.create(
                    account=to_account, amount=amount, transaction_type="TRANSFER_IN"
                )

                return Response(
                    {"message": "Transfer successful"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST
                )

        except Account.DoesNotExist:
            return Response(
                {"error": "Invalid account ID"}, status=status.HTTP_400_BAD_REQUEST
            )
