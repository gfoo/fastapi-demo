## How to start to dev

Create a .env file contaning dev configurations (empty database ready to use) :

```
PROJECT_NAME="fastapi_demo"
ADMIN_EMAIL="admin@nowhere.org"
ADMIN_PASSWORD="admin"
SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/fastapi_demo"
# Generate a secret key for jose JWT
# $ openssl rand -hex 32
SECRET_KEY="d613f7874dea70e21ccbac61247368b61c16247a2a4ed0a8a645aeb608d085e6"
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

Create a python venv:

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Init database:

```shell
$ alembic upgrade head
```

Launch API:

```shell
$ uvicorn main:app --reload
```

Doc : http://localhost:8000/docs

## Helpfull commands

```
# re-init db
$ psql -U postgres -h localhost -c "drop database fastapi_demo"
$ psql -U postgres -h localhost -c "create database fastapi_demo"

# generate new mapping according to last models
$ alembic revision --autogenerate -m "bla bla"
```
