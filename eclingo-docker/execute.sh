#!/bin/bash

IMAGE_NAME=eclingo-benchmark
CONTAINER_NAME=eclingo-container

# docker build -t $IMAGE_NAME .
docker build -t $IMAGE_NAME -f ezsmt-comparison/Dockerfile .

if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
    docker rm $CONTAINER_NAME
fi

docker run --name $CONTAINER_NAME $IMAGE_NAME

docker cp $CONTAINER_NAME:/root/eclingo-benchmark/log.txt .