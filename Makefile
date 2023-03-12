all: down up

build:
	podman-compose build

up:
	podman-compose up --build -d --remove-orphans

down:
	podman-compose down

logs:
	podman-compose logs
