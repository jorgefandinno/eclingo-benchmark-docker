### Clone repo with submodules:
```
git clone --recurse-submodules <repository-url>
```
OR
```
git clone <repository-url>
git submodule init
git submodule update
```

### Command to build the docker file:
```
docker build . -t <image-name>
```

### Command to run the docker:
```
docker run -it <image-name>
```
