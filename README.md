## Heroku demo

https://fastapi-demo-gfoo.herokuapp.com/docs

Users :

- `admin@nowhere.org / admin`
- `demo@nowhere.org / demo`

(possibly wait a while if service is stopped...)

## Local dev

(Frontend available [here](https://github.com/gfoo/react-demo))

Create a .env file contaning dev configurations (empty database ready to use) :

```
#
# required
#
PROJECT_NAME="fastapi_demo"
SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/fastapi_demo"
# Generate a secret key for jose JWT
# $ openssl rand -hex 32
SECRET_KEY="d613f7874dea70e21ccbac61247368b61c16247a2a4ed0a8a645aeb608d085e6"
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
ADMIN_EMAIL="admin@nowhere.org"
ADMIN_PASSWORD="admin"
#
# optional
#
DEMO_EMAIL="demo@nowhere.org"
DEMO_PASSWORD="demo"

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
