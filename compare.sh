#!/bin/bash

# arguments to provide when building image
BUILD_ARGS=""
for arg in $@; do
    BUILD_ARGS+="$arg " 
done

# set variables
IMAGE_NAME=eclingo
SOLVER_1=eclingo
SOLVER_2=eclingo-old

# build image
BUILD_COMMAND="docker build $BUILD_ARGS -t $IMAGE_NAME ."
printf "Running: $BUILD_COMMAND\n"
eval "$BUILD_COMMAND"

# set container name
CONTAINER_NAME=${IMAGE_NAME}-container

# remove container if it exists
if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
    printf "\ndocker container with name \"$CONTAINER_NAME\" exists, so removing the container\n"
    DELETE_COMMAND="docker rm $CONTAINER_NAME"
    eval "$DELETE_COMMAND"
fi

# run container
RUN_COMMAND="docker run --name $CONTAINER_NAME -e max_instances=2 -e benchmark=yale $IMAGE_NAME"
printf "\nRunning: $RUN_COMMAND\n"
eval "$RUN_COMMAND"

# copy results from container to host
mkdir -p results
docker cp $CONTAINER_NAME:/root/run-benchmark/matching_instances.txt results/
docker cp $CONTAINER_NAME:/root/run-benchmark/non_matching_instances.txt results/
docker cp $CONTAINER_NAME:/root/run-benchmark/timed_out_instances.txt results/
docker cp $CONTAINER_NAME:/root/run-benchmark/log.txt results/
docker cp $CONTAINER_NAME:/root/run-benchmark/analysis/ results/

mkdir -p results/$SOLVER_1
docker cp $CONTAINER_NAME:/root/run-benchmark/running/benchmark-tool-$SOLVER_1/experiments/results/$SOLVER_1/$SOLVER_1.ods results/$SOLVER_1/
docker cp $CONTAINER_NAME:/root/run-benchmark/running/benchmark-tool-$SOLVER_1/output/project/zuse/results/suite/ results/$SOLVER_1/

mkdir -p results/$SOLVER_2
docker cp $CONTAINER_NAME:/root/run-benchmark/running/benchmark-tool-$SOLVER_2/experiments/results/$SOLVER_2/$SOLVER_2.ods results/$SOLVER_2/
docker cp $CONTAINER_NAME:/root/run-benchmark/running/benchmark-tool-$SOLVER_2/output/project/zuse/results/suite/ results/$SOLVER_2/

printf "\nAll results are stored in results directory\n"
