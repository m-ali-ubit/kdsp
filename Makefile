# Starts all the containers
up:
	docker-compose -f local.yml up

# Destroys all the containers and rebuilds them
upnew:
	docker-compose -f local.yml build
	docker-compose -f local.yml up -d django
	docker exec django ../entrypoint python manage.py makemigrations
	docker exec django ../entrypoint python manage.py migrate
	docker-compose -f local.yml down


# Ends all the containers
down:
	docker-compose -f local.yml down

# runs django test
test:
	 docker-compose -f local.yml run django pytest

# runs migrations inside the django container
migrate:
	docker exec -it django ../entrypoint python manage.py migrate

# creates new migrations if there is any model changes
migrations:
	docker exec -it django ../entrypoint python manage.py makemigrations

# creates a django user with all rights and privileges
superuser:
	docker exec -it django ../entrypoint python manage.py createsuperuser

# access django container shell
shell:
	docker exec -it django ../entrypoint /bin/sh

# opens up a terminal and starts the django shell
djangoshell:
	docker exec -it django ../entrypoint python manage.py shell_plus

# runs black formatting on all project files except migrations
black:
	black . --exclude ^.*\b(migrations)\b.*$

# sorts all the import commands in all python files
sort:
	isort .

# runs pre-commit on whole project and checks/fix formatting, styling and linting
clean:
	pre-commit run --all-files
