runserver:
	python manage.py runserver

test:
	python manage.py test --noinput

testuser:
	python manage.py createtestuser

superuser:
	python manage.py createsuperuser

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

format:
	isort .
	brunette ../src --config=setup.cfg

dev:
	git checkout dev
	git pull origin dev
	pip install -r ../etc/requirements.txt
	python manage.py migrate

check:
	python manage.py makemigrations --dry-run --check
	python manage.py test --noinput
	isort --check-only --diff .
	brunette ../src --check --diff --config=setup.cfg

ilocal:
	pip install -r ../etc/local.requirements.txt

iprod:
	pip install -r ../etc/production.requirements.txt

init:
	make ilocal
	cp ../etc/env_example ./app/.env
	cp ../etc/env_example.py ./app/env.py

reset:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	python manage.py makemigrations
	isort .
	brunette ../src --config=setup.cfg
	python manage.py migrate

celery:
	celery -A app worker -B -l info

beat:
	celery -A app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

data:
	python manage.py loaddata default
