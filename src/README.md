# Starter Project Backend

Commands:

```
make dev
```
Goes to dev branch and update last changes (migrate and install packages).

```
make migrations
```
python manage.py makemigrations
```
make migrate
```
python manage.py migrate

```
make check
```
Run tests, check migrations and format for github action and local review
```
make test
```
Run tests for server side

```
make format
```
Auto format with brunette (black).

```
make ilocal
or
make iprod
```
Install environment packages (local or production).


## Running this project.

- Create and activate virtual environment.
- Copy etc/env_example.py as app/env.py
- Copy etc/env_example as app/.env
- Run ```make dev```