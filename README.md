interBANK
=====================

![alt text](http://marcin86.pythonanywhere.com/static/InterBANK.PNG)

Overview
--------

interBANK is simple banking web application created using Django REST Framework.

Requirements:
-------------

	Python 3.10.8 (3.x.x working in Docker)
	Django 4.2
    Djangorestframework==3.14.0

Installation:
-------------


	Create new folder "interBANK" and open it:
	git clone https://github.com/marcin86junior/MegaPictureUploadREST.git .
	python -m venv myvenv
	.\myvenv\Scripts\activate
	pip install -r requirements.txt
	cd django_rest_imageupload_backend\
	python manage.py migrate
	python manage.py migrate --run-syncdb
	python manage.py loaddata group.json users.json data.json
	python .\manage.py runserver
	http://127.0.0.1:8000/api/
	*python manage.py createsuperuser (marcin/123)


Testing:
--------

	python manage.py test
	coverage run --source='.' --omit='*migrations*,*init*,*wsgi*,*asgi*,*urls*,*manage*,*admin*,*apps*,*settings*,*test*,*seriali*' manage.py test
	coverage report (or) coverage html


Docker:
-------

	Create new folder "interBANK" and open it:
	git clone https://github.com/marcin86junior/MegaPictureUploadREST.git .
	cd django_rest_imageupload_backend\
	"Open Doker Desktop"
	format file in \django_rest_imageupload_backend\docker-entrypoint.sh    CRLF->LF
	docker-compose up
	http://127.0.0.1:8000/api/
	Test:
	docker-compose run web python3 manage.py test


Fixtures
--------


	Data included in fixtures:

	User / Password / Assigned group / Added pictures to model
	b1 / 123 / Basic / 2
	p2 / 123 / Premium / 2
	e3 / 123 / Enterprice/ 2 
	c4 / 123 / Custom/ 2


Issues
------


	At the moment there are few issuse:

	- aaa
	- bbb