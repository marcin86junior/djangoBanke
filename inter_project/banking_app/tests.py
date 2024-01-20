from django.test import TestCase
from django.contrib.auth.models import User
from .models import Account, Transaction
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal


class UserViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_main_page_display_before_loged(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.content.decode('utf-8'))
        self.assertIn('Register', response.content.decode('utf-8'))

    def test_create_user(self):
        user_data = {
            'username': 'testuser',
            'password': '123',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

        response = self.client.post('/api/user_create/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_main_page_display_after_login(self):
        user = User.objects.create_user(username='testuser', password='123', email='test@example.com')
        self.client.login(username=user.username, password='123')
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.content.decode('utf-8'))
        self.assertIn('Deposit/Withdraw', response.content.decode('utf-8'))
        self.client.logout()

    def test_internal_transaction(self):
        user_data = {
            'username': 'testuser',
            'password': '123',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

        response = self.client.post('/api/user_create/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='testuser')
        account = user.account
        self.client.login(username=user.username, password='123')

        transaction_data = {
            "account": 1,
            'amount': 100,
            'transaction_type': 'DEPOSIT',
        }

        response = self.client.post('/api/transaction/', transaction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Transaction.objects.filter(account=account).exists())
        
        # Retrieve the updated account balance
        updated_balance = Account.objects.get(id=account.id).balance
        expected_balance = 100
        self.assertEqual(updated_balance, Decimal(expected_balance))
        self.client.logout()

    def test_external_transaction(self):
        user_data = {
            'username': 'testuser',
            'password': '123',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
        }

        response = self.client.post('/api/user_create/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='testuser')
        account = user.account
        self.client.login(username=user.username, password='123')

        user_data_2 = {
            'username': 'testuser2',
            'password': '123',
            'email': 'test2@example.com',
            'first_name': 'Test2',
            'last_name': 'User2',
        }

        response = self.client.post('/api/user_create/', user_data_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        transaction_data = {
            "account": 1,
            'amount': 100,
            'transaction_type': 'DEPOSIT',
        }

        response = self.client.post('/api/transaction/', transaction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Transaction.objects.filter(account=account).exists())
        
        # Retrieve the updated account balance
        updated_balance = Account.objects.get(id=account.id).balance
        expected_balance = 100
        self.assertEqual(updated_balance, Decimal(expected_balance))

        # We need collect account_no from model Account ID 1 and 2 becase it randomized (not 1,2)
        from_account_no = Account.objects.get(id=1).account_no
        to_account_no = Account.objects.get(id=2).account_no

        # External transfer from the first account to the second account
        transfer_data = {
            'from_account_id': from_account_no,
            'to_account_id': to_account_no,
            'amount': 50,
        }
        response = self.client.post('/api/transfer/', transfer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the updated balances of the accounts
        updated_balance_from_after_transfer = Account.objects.get(id=1).balance
        expected_balance_from_after_transfer = 50
        self.assertEqual(updated_balance_from_after_transfer, Decimal(expected_balance_from_after_transfer))

        updated_balance_to_after_transfer = Account.objects.get(id=2).balance
        expected_balance_to_after_transfer = 50
        self.assertEqual(updated_balance_to_after_transfer, Decimal(expected_balance_to_after_transfer))

        # Check if the transaction records are created
        # self.assertTrue(Transaction.objects.filter(account=from_account_no, transaction_type='TRANSFER_OUT').exists())
        # self.assertTrue(Transaction.objects.filter(account=to_account_no, transaction_type='TRANSFER_IN').exists())

        self.client.logout()
