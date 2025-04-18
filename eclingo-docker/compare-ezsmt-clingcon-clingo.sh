#!/bin/bash

# arguments to provide when building image
BUILD_ARGS=""
for arg in $@; do
    BUILD_ARGS+="$arg " 
done

# set variables
IMAGE_NAME=ezsmt-clingcon-clingo
SOLVER_1=ezsmt
SOLVER_1_NAME=ezsmt
SOLVER_2=clingcon
SOLVER_2_NAME=clingcon
SOLVER_3=clingo
SOLVER_3_NAME=clingo

# build image
BUILD_COMMAND="docker build $BUILD_ARGS -t $IMAGE_NAME -f ezsmt-comparison/Dockerfile ."
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
RUN_COMMAND="docker run --name $CONTAINER_NAME $IMAGE_NAME"
printf "\nRunning: $RUN_COMMAND\n"
eval "$RUN_COMMAND"

# copy results from container to host
mkdir -p results
docker cp $CONTAINER_NAME:/root/eclingo-benchmark/matching_instances.txt results/
docker cp $CONTAINER_NAME:/root/eclingo-benchmark/non_matching_instances.txt results/
docker cp $CONTAINER_NAME:/root/eclingo-benchmark/timed_out_instances.txt results/
docker cp $CONTAINER_NAME:/root/eclingo-benchmark/log.txt results/
docker cp $CONTAINER_NAME:/root/eclingo-benchmark/analysis/ results/

mkdir -p results/$SOLVER_1_NAME
docker cp $CONTAINER_NAME:/root/eclingo-benchmark/running/benchmark-tool-$SOLVER_1_NAME/experiments/results/$SOLVER_1_NAME/$SOLVER_1_NAME.ods results/$SOLVER_1_NAME/
# docker cp $CONTAINER_NAME:/root/eclingo-benchmark/running/benchmark-tool-$SOLVER_1_NAME/output/project/zuse/results/suite/ results/$SOLVER_1_NAME/

mkdir -p results/$SOLVER_2_NAME
docker cp $CONTAINER_NAME:/root/eclingo-benchmark/running/benchmark-tool-$SOLVER_2_NAME/experiments/results/$SOLVER_2_NAME/$SOLVER_2_NAME.ods results/$SOLVER_2_NAME/
# docker cp $CONTAINER_NAME:/root/eclingo-benchmark/running/benchmark-tool-$SOLVER_2_NAME/output/project/zuse/results/suite/ results/$SOLVER_2_NAME/

mkdir -p results/$SOLVER_3_NAME
docker cp $CONTAINER_NAME:/root/eclingo-benchmark/running/benchmark-tool-$SOLVER_3_NAME/experiments/results/$SOLVER_3_NAME/$SOLVER_3_NAME.ods results/$SOLVER_3_NAME/
# docker cp $CONTAINER_NAME:/root/eclingo-benchmark/running/benchmark-tool-$SOLVER_3_NAME/output/project/zuse/results/suite/ results/$SOLVER_3_NAME/


printf "\nAll results are stored in results directory\n"