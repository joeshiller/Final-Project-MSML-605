#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Define variables for image name and container name
IMAGE_NAME="msml605-final"
CONTAINER_NAME="msml605-final-container"
HOST_WORK_DIR="$PROJECT_ROOT/"
CONTAINER_WORK_DIR="/work"
VENV_VOLUME_NAME="msml605-final-volume"

# Check if the container is already running
if [ "$(docker ps --all --quiet --filter name=$CONTAINER_NAME)" ]; then
    echo "Stopping the currently running container $CONTAINER_NAME..."
    docker stop $CONTAINER_NAME
    echo "Removing the stopped container $CONTAINER_NAME..."
    docker rm $CONTAINER_NAME
fi

# Run the Docker container with interactive bash
echo "Running the Docker container $CONTAINER_NAME..."
docker run --interactive --rm --name $CONTAINER_NAME \
    --volume "$HOST_WORK_DIR:$CONTAINER_WORK_DIR" \
    --volume "$VENV_VOLUME_NAME:$CONTAINER_WORK_DIR/.venv" \
    -w "$CONTAINER_WORK_DIR" \
    $IMAGE_NAME:latest \
    $@
