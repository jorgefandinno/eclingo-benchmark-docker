### Clone repository:
```
git clone <repository-url>
cd eclingo-benchmark-docker/eclingo-docker/
```

### Command to build the docker image:
```
# In directory with dockerfile
docker build -t benchmark-eclingo .
```

### Command to run the docker container:
```
# -i for interactive, -t for terminal
docker run -it benchmark-eclingo
```

### Command to save build logs to a log file
```
# --no-cache ignores cached layers
docker build -t benchmark-eclingo --no-cache --progress=plain . &> build.log
```
