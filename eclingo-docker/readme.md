Command to build the docker file:
docker build . -t benchmark-eclingo --build-arg GIT_ACCESS_TOKEN=<git-access-token>

Command to run the docker
docker run -it benchmark-eclingo