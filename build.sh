#!/bin/bash

echo "Restarting..."
podman stop persephone
podman build -f Containerfile -t persephone
podman run -d --name=persephone persephone
echo "Waiting to verify successful start..."
sleep 5

if podman ps | grep -q persephone; then
    echo "persephone still running :)"
    podman logs persephone
    exit 0
else
    echo "persephone isn't running anymore :("
    podman logs persephone
    exit 1
fi
