#!/usr/bin/env bash

# Define variables for image name and version
IMAGE_NAME="msml605-final"
VERSION="latest"

# Build the Docker image
docker build -t $IMAGE_NAME:$VERSION .

echo "Docker image $IMAGE_NAME:$VERSION built successfully."
