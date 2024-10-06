# Download base image ubuntu 22.04
FROM ubuntu:22.04
# LABEL about the custom image
LABEL maintainer="kdhakal@unomaha.edu"
LABEL version="0.1"
LABEL description="This is a custom Docker Image for benchmarking solvers for Epistemic Logic Programs (ELPs)"
# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# Update Ubuntu Software repository
RUN apt update
# Install conda
WORKDIR /root/
RUN apt install -y wget
RUN apt install -y git
RUN apt install -y python2
RUN apt install -y libnuma-dev
RUN mkdir -p /root/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda3/miniconda.sh
RUN chmod +x ~/miniconda3/miniconda.sh
RUN bash /root/miniconda3/miniconda.sh -b -u -p /root/miniconda3
RUN rm -rf /root/miniconda3/miniconda.sh
RUN /root/miniconda3/bin/conda init bash

# Copy benchmark tool and create conda environment
COPY eclingo-benchmark /root/eclingo-benchmark/
WORKDIR /root/eclingo-benchmark/
# RUN sed -i 's/runsolver/eclingo/' run-benchmark.xml

# set bash (interactive) as the default shell
# SHELL ["/bin/bash", "-i", "-c"]

# create and activate conda env reif, install eclingo new and run benchmark
RUN /root/miniconda3/bin/conda env create -f envs/environment_eclingo_reif.yml
RUN echo "conda activate eclingo_reif" >> /root/.bashrc \
    && . /root/.bashrc \
    && git clone https://github.com/jorgefandinno/eclingo.git \
    && cd eclingo/ \
    && pip install . \
    && cd .. \
    && rm -r eclingo \
    && nohup ./run.sh eclingo

# create and activate conda env old, install eclingo old and run benchmark
RUN /root/miniconda3/bin/conda env create -f envs/environment_eclingo_old.yml
RUN echo "conda activate eclingo_old" >> /root/.bashrc \
    && . /root/.bashrc \
    && git clone https://github.com/potassco/eclingo.git \
    && cd eclingo/ \
    && pip install . \
    && cd .. \
    && nohup ./run.sh eclingo-old \
    && python verify.py