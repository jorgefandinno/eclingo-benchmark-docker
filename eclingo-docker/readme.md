Recursive clone the repo
git clone --recurse-submodules <repository-url>

Command to build the docker file:
docker build . -t benchmark-eclingo

Command to run the docker
docker run -it benchmark-eclingo