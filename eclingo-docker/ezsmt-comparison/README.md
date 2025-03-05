# How to build and run ezsmt image from Dockerfile

_Make sure you are in the path: **eclingo-benchmark-docker/eclingo-docker/ezsmt-comparison/**_


**Build ezsmt image:**
```
cd ..
docker build -t <image-name:tag> -f ezsmt-comparison/Dockerfile .
docker build -t ezsmt -f ezsmt-comparison/Dockerfile .
```

**Save build logs to a log file:**
```
# --no-cache ignores cached layers
docker build -t <image-name:tag> --no-cache --progress=plain . &> build.log
docker build -t ezsmt --no-cache --progress=plain . &> build.log
```

**Run image container:**
```
# -e is flag for overwriting environment variable
docker run [-e <variable-name>=<value>] <image-name:tag>
docker run ezsmt

# -i for interactive, -t for terminal
docker run -it <image-name:tag> /bin/bash
docker run -it ezsmt /bin/bash
```

**Save container as image**
```
docker commit <container-id> <new-image-name:tag>
docker commit cebe1c44fb02 new-ezsmt
```
