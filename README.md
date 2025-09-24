djangoBanke
=====================

![alt text](https://github.com/marcin86junior/interBANK/blob/main/readme.PNG)

Overview
--------

interBANK is simple banking web application created using Django REST Framework.

Requirements:
-------------

	Python 3.10.8 (3.10.x working with Docker)
	Django 4.2
    Djangorestframework==3.14.0

Installation:
-------------


	Create new folder "interBANK" and open it:
	git clone https://github.com/marcin86junior/interBANK .
	python -m venv myvenv
	.\myvenv\Scripts\activate
	pip install -r requirements.txt
	cd inter_project\
	python manage.py migrate
	add SECRET_KEY = 'xxx' in settings.py
	python .\manage.py runserver
	http://127.0.0.1:8000/


Testing:
--------

	python manage.py test


Docker:
-------

	Create new folder "interBANK" and open it:
	git clone https://github.com/marcin86junior/interBANK .
	cd inter_project\
	"Open Doker Desktop"
	change format file in \inter_project\docker-entrypoint.sh    CRLF->LF (save!)
	add SECRET_KEY = 'xxx' in settings.py
	docker-compose up
	http://127.0.0.1:8000/
	Test:
	docker-compose run web python3 manage.py test


Instructions:
-------


    Register on the Website:
        Go to the main page http://127.0.0.1:8000/ to register an account.
        Navigate to the "Register" section http://127.0.0.1:8000/api/user_create/

    Log In:
        After registering, log in to your account using your credentials.
        Navigate to the "Login" section http://127.0.0.1:8000/api/api-auth/login/

    Check Account Balance:
        To check your account balance, go to "My Account":
            Visit http://127.0.0.1:8000/api/account/
            Your current account balance will be displayed on the dashboard.

    Check Transaction List:
        To check your transactions, go to "Transaction List":
            Visit http://127.0.0.1:8000/api/transactions_list/
            Your current account balance will be displayed on the dashboard.

    Deposit Funds:
        Navigate to the "Internal Deposit/Withdraw" section on http://127.0.0.1:8000/api/transaction/
        Follow the provided instructions to complete the deposit transaction.

    Outside Transfer:
        Navigate to the "Outside Transfer" section on http://127.0.0.1:8000/api/transfer/
        Follow the provided instructions to complete the transfer transaction.


Tests:
-------


    Unauthenticated User Page Test:
        Navigate to the main page [http://127.0.0.1:8000/] without logging in.
        Confirm that the page is accessible and displays relevant information for unauthenticated users.

    User Registration Test:
        Go to the "Register" section [http://127.0.0.1:8000/api/user_create/].
        Complete the registration process with valid credentials.
        Verify that the registration is successful and that the user can now log in.
	
	Main Page After Login Test:
        Log in using valid credentials.
        Navigate to the main page [http://127.0.0.1:8000/] after logging in.
        Confirm that the page is accessible and displays relevant information for authenticated users.

    Internal Transfer Test:
        Visit the "Internal Deposit/Withdraw" section [http://127.0.0.1:8000/api/transaction/].
        Follow the provided instructions to complete an internal fund transfer.
        Confirm that the transaction is reflected accurately in the user's account balance.

    Two Users Registration and Account Transfer Test:
        Register two users using the registration process.
        Log in with the credentials of the first user and initiate a transfer to the second user's account.
        Log in with the credentials of the second user and confirm that the funds have been successfully transferred.


Todo list:
-------


    Add html template for My account [OK]
    Add html template for User registration [finish: /api/user_create/register_form/]
    Add html template for Internal transfer 
    Add html template for Status
    Fix for docker: docker-compose run web python3 manage.py test
    Fix for docker: remove double requirements.txt in folders
    Fix for docker: remove postgres from docker-compose.yml
    Add to Transaction model: balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    Add to Account model: currency [only PLN]
