# clogs
Prototype geogirafe backend with Django Web Framework

:warning This is NOT production ready :warning


## Start playing

1. Clone this repository

2. Execute following commands

```

cp .env.example .env
docker compose build && docker compose up -d
python3 manage.py collectstatic --no-input
docker compose exec clogs migrate
docker compose exec python manage.py populate_users

```

3. Go to http://localhost:9051 and you should see the welcome page.
