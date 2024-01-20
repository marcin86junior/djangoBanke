interBANK
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
	change format file in \inter_project\docker-entrypoint.sh    CRLF->LF
	docker-compose up
	http://127.0.0.1:8000/
	Test:
	docker-compose run web python3 manage.py test
