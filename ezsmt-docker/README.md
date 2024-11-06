### Build EZSMT dockerfile:
```
cd eclingo-benchmark-docker/ezsmt-docker
docker build -t ezsmt .
```

### Command to run the docker container:
```
# -i for interactive, -t for terminal
docker run -it ezsmt
```

### EZSMT Description:
```
# in container terminal
ezsmt -h
```

### Run Examples:
```
# in container terminal
cd examples
ezsmt routingMin/encodings/RoutingMin.lp routingMin/instances/d40.1
```