#!/bin/bash

# For eclingo comparison
IMAGE_NAME=eclingo-benchmark

# For ezsmt comparison
# IMAGE_NAME=ezsmt

CONTAINER_NAME=${IMAGE_NAME}-container

BUILD_ARGS=""
for arg in $@; do
    BUILD_ARGS+="$arg " 
done

# For eclingo comparison
docker build $BUILD_ARGS -t $IMAGE_NAME .

# For ezsmt comparison
# docker build $BUILD_ARGS -t $IMAGE_NAME -f ezsmt-comparison/Dockerfile .

if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
    docker rm $CONTAINER_NAME
fi

docker run --name $CONTAINER_NAME $IMAGE_NAME

mkdir -p results
docker cp $CONTAINER_NAME:/root/eclingo-benchmark/log.txt results/
docker cp $CONTAINER_NAME:/root/eclingo-benchmark/analysis/ results/

echo "All results are stored in results directory"
