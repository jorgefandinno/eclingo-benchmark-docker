#!/bin/bash

echo "Arguments:"

for ARG in "$@"
do
    KEY="${ARG%%=*}"   # Extract part before '='
    VALUE="${ARG#*=}"   # Extract part after '='

    # Remove '--' prefix from the key
    KEY="${KEY#--}"

    echo "$KEY: $VALUE"
    export "$KEY"="$VALUE"
done

echo ""

eval "$(conda shell.bash hook)"
