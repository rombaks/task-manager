# TaskManager 
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Frombaks%2FTaskManager%2Fbadge%3Fref%3Ddevelop&style=flat)](https://actions-badge.atrox.dev/rombaks/TaskManager/goto?ref=develop) 
[![Coverage Status](https://coveralls.io/repos/github/rombaks/TaskManager/badge.svg?branch=develop&kill_cache=1)](https://coveralls.io/github/rombaks/TaskManager?branch=develop)
---

### Project features

Project helps you to get things done! It provides:

- user roles with different permissions (Developer, Manager and Admin);
- task with a variety of states (from new to achieved);
- email notification;
- background user reports generation;
- admin panel for management.

### Usage

-   Clone the repo.

```
git clone git@github.com:rombaks/task-manager.git
```

-   Add your credentials to `.env` file for a local development
```
DJANGO_SECRET_KEY=your_secret

DATABASE_NAME=your_secret
DATABASE_USER=your_secret
DATABASE_PASSWORD=your_secret
DATABASE_HOST=your_secret
DATABASE_PORT=your_secret

REDIS_HOST=your_secret
REDIS_PORT=your_secret

POST_SERVER_ITEM_ACCESS_TOKEN=your_secret

EMAIL_USE_SSL=0
EMAIL_USE_TLS=1
EMAIL_HOST=your_secret
EMAIL_HOST_USER=your_secret
EMAIL_HOST_PASSWORD=your_secret
EMAIL_PORT=your_secret

DEBUG=False
```

-   Build docker-compose from project root directory

```
docker-compose build 
```

-   To run `bash` in our container

```
docker-compose run --rm api bash
```

-   Make initial database migrations in `bash`

```
./manage.py makemigrations
./manage.py migrate
```

-   Create superuser in `bash` for access to the admin panel

```
./manage.py createsuperuser
```

-   To connect to `PostgreSQL` interactive terminal

```
docker-compose exec db psql -U postgres
```

-   Run app on http://localhost:8000 (set port in `docker-compose.yml` if necessary)

```
docker-compose up
```

---

### Additional info

- API: Django REST framework. Docs http://localhost:8000/swagger/
- Admin panel: Django admin  http://localhost:8000/admin/
- DateBase: PostrgeSQL
- Asyncronous Request-Reply: Celery + Redis
- Tasks monitoring: Flower
- Dependency manager: Poetry
- Code formatter: Black
- Tests: PyTest + Factory Boy + Coveralls
- CI/CD: GitHub Actions
- Monitoring: Rollbar + NewRelic
- Deployment ready: Heroku
