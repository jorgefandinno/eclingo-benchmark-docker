#!/bin/bash

IMAGE_NAME=ezsmt
CONTAINER_NAME=ezsmt-container

BUILD_ARGS=""
for arg in $@; do
    BUILD_ARGS+="$arg " 
done

docker build $BUILD_ARGS -t $IMAGE_NAME .
# docker build $BUILD_ARGS -t $IMAGE_NAME -f ezsmt-comparison/Dockerfile .

if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
    docker rm $CONTAINER_NAME
fi

docker run --name $CONTAINER_NAME $IMAGE_NAME

docker cp $CONTAINER_NAME:/root/eclingo-benchmark/log.txt .
