### Clone repository:
```
git clone <repository-url>
cd eclingo-benchmark-docker/eclingo-docker/
```

### Command to build the docker image:
```
# In directory with dockerfile
docker build -t <image-name:tag> .
```

### Command to run the docker container:
```
# -i for interactive, -t for terminal
docker run -it <image-name:tag>
```

### Command to save build logs to a log file
```
# --no-cache ignores cached layers
docker build -t <image-name:tag> --no-cache --progress=plain . &> build.log
```
