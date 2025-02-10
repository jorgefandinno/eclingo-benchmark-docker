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

# create conda environments
RUN /root/miniconda3/bin/conda env create -f envs/environment_eclingo_reif.yml
RUN /root/miniconda3/bin/conda env create -f envs/environment_eclingo_old.yml

# activate eclingo_reif conda environment, install eclingo new and run benchmark
RUN echo "conda activate eclingo_reif" >> /root/.bashrc \
    && . /root/.bashrc \
    && git clone https://github.com/jorgefandinno/eclingo.git \
    && cd eclingo/ \
    && pip install . \
    && cd .. \
    && rm -r eclingo \
    && git clone https://github.com/potassco/eclingo.git \
    && echo "Running eclingo_reif benchmarks" \
    && ./run.sh eclingo --max-instances=2 --benchmark=all > log.txt

# activate eclingo_old conda environment, install eclingo old and run benchmark
RUN echo "conda activate eclingo_old" >> /root/.bashrc \
    && . /root/.bashrc \
    && cd eclingo/ \
    && git checkout tags/v0.2.1 \
    && pip install . \
    && cd .. \
    && echo "Running eclingo_old benchmarks" \
    && ./run.sh eclingo-old --max-instances=2 --benchmark=all >> log.txt \
    && python examine_output.py -s1 eclingo -s2 eclingo -s2n eclingo-old -l 10 >> log.txt