# Download base image ubuntu 22.04
FROM ubuntu:22.04
# LABEL about the custom image
LABEL maintainer="jfandinno@unomaha.edu"
LABEL version="0.1"
LABEL description="This is a custom Docker Image for solvers for Epistemic Logic Programs (ELPs)"
# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive
# Update Ubuntu Software repository
RUN apt update
# Install conda
WORKDIR ~/
RUN apt install -y wget
RUN apt install -y git
RUN mkdir -p ~/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
RUN chmod +x ~/miniconda3/miniconda.sh
RUN bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
RUN rm -rf ~/miniconda3/miniconda.sh
RUN ~/miniconda3/bin/conda init bash
RUN echo "conda activate" >> ~/.bashrc
# Install EP-ASP
RUN ~/miniconda3/bin/conda create -y -n ep-asp -c conda-forge python=3.7 clingo=5.4.0
RUN git clone --depth 1 https://github.com/krr-uno/EP-ASP.git

ENTRYPOINT ["bash"]