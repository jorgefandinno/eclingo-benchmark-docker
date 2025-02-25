# How to build and run ezsmt Dockerfile

_Make sure you are in the path: **eclingo-benchmark-docker/eclingo-docker/ezsmt-comparison/**_


**Building Dockerfile:**
```
cd ..
docker build -t <image-name:tag> -f ezsmt-comparison/Dockerfile .
docker build -t ezsmt -f ezsmt-comparison/Dockerfile .
```


**Running the image container:**
```
# -e is flag for overwriting environment variable
docker run [-e <variable-name>=<value>] <image-name:tag>
docker run ezsmt

# -i for interactive, -t for terminal
docker run -it <image-name:tag> /bin/bash
docker run -it ezsmt /bin/bash
```
