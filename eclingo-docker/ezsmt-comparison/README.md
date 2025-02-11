# How to build and run ezsmt Dockerfile

_Make sure you are in the path: **eclingo-benchmark-docker/eclingo-docker/ezsmt-comparison/**_


**Building Dockerfile:**
```
cd ..
docker build -t <image-name:tag> -f ezsmt-comparison/Dockerfile .
```


**Running the image:**
```
docker run -it <image-name:tag>
```

**Show the logs:**
```
cat log.txt
```
