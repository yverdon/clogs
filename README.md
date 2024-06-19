# clogs
Prototype geogirafe backend with Django Web Framework

:warning: This is NOT production ready :warning:

## Features

- Edit geogirafe themes configuration from admin, including geometric feature edition
- Import themes configuration from  existing geoportal
- Users and roles management with Django built-in functionnalities
- Historical tracking of configuration changes with possiblity to revert
- Expose themes.json thanks to django-ninja
- Demo geogirage viewer connected to ninja's endpoint

![image](https://github.com/monodo/clogs/assets/3356536/739a69dd-879d-4589-9735-62922aedf08f)




https://github.com/monodo/clogs/assets/3356536/41c3300b-1eb9-466f-bd2f-2066032aada5


## Start playing

1. Clone this repository

2. Execute following commands

```

cp .env.example .env
docker compose build && docker compose up -d
python3 manage.py collectstatic --no-input
docker compose exec clogs migrate
docker compose exec python manage.py populate_users
docker compose exec python manage.py populate_themes

```

or

Duplicate your prefered geoportal
```
cp .env.example .env
docker compose build && docker compose up -d
docker compose exec clogs scripts/demo.sh
```

Go to http://localhost:9051 and you should see the welcome page.

4. Start de geogirafe demo


```
cd geogirafe-viewer
npm start
```
Go to http://localhost:5173 and you should see the welcome page.






### Linting

We use [pre-commit](https://pre-commit.com/) as code formatter. Just use the following command to automatically format your code when you commit:

```
$ pip install pre-commit
$ pre-commit install
```

If you wish to run it on all files:

```
$ pre-commit run --all-files
```

### Dependency management

Dependencies are managed with [`pip-tools`](https://github.com/jazzband/pip-tools).

### Installing packages

To install a new package, add it to `requirements.in`, without pinning it to a
specific version unless needed. Then run:

```
docker compose exec clogs pip-compile requirements.in
docker compose exec clogs pip-compile requirements_dev.in
docker compose exec clogs pip install -r requirements.txt
docker compose exec clogs pip install -r requirements_dev.txt
```

Make sure you commit both the `requirements.in` and the `requirements.txt` files.
And the `requirements_dev.in` and the `requirements_dev.txt` files.

### Upgrading packages

To upgrade all the packages to their latest available version, run:

```
docker compose exec clogs pip-compile -U requirements.in
docker compose exec clogs pip install -r requirements.txt
```

To upgrade only a specific package, use `pip-compile -P <packagename>`.
The following commands will upgrade Django to its latest version, making sure
it's compatible with other packages listed in the `requirements.in` file:

```
docker compose exec web pip-compile -P django requirements.in
docker compose exec web pip install -r requirements.txt
```

## Documenting models

In order to generate the model documentation, run:
```
docker compose run clogs scripts/generate_models_diagram.sh
```
