export PREFIX := ,
all: down prune up logs

build:
	podman-compose build

up:
	podman-compose up --build -d

down:
	podman-compose down

logs:
	podman-compose logs

prune:
	podman image prune -af

enter:
	podman run --secret bot_token --secret owner_id --secret personality --secret openai_api_key --secret dezgo_api_key --secret google_api_key --secret google_engine_id -it persephone /bin/bash
