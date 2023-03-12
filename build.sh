#!/bin/bash

echo "Restarting..."
docker compose down
docker compose up --build -d --remove-orphans
echo "Waiting to verify successful start..."
sleep 5

if docker compose ls | grep -q ^persephone; then
    echo "persephone still running :)"
    docker compose logs
    exit 0
else
    echo "persephone isn't running anymore :("
    docker compose logs 
    exit 1
fi
