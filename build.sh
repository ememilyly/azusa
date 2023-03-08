#!/bin/bash

echo "Restarting..."
docker compose down
docker compose up --build -d --remove-orphans
echo "Waiting to verify successful start..."
sleep 5

if [[ `docker compose ls | grep -q ^azusa` ]]; then
    echo "azusa isn't running anymore :("
    docker compose logs 
    exit 1
else
    echo "azusa still running :)"
    exit 0
fi
