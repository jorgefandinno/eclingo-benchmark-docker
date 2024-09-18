# Download base image ubuntu 22.04
FROM ubuntu:22.04
# LABEL about the custom image
LABEL maintainer="kdhakal@unomaha.edu"
LABEL version="0.1"
LABEL description="This is a custom Docker Image for benchmarking solvers for Epistemic Logic Programs (ELPs)"
# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ACCESS_TOKEN

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

# Clone benchmark tool and create conda environment
RUN git clone https://${GIT_ACCESS_TOKEN}@github.com/jorgefandinno/eclingo-benchmark.git
WORKDIR /~/eclingo-benchmark/
RUN sed -i 's/runsolver/eclingo/' run-benchmark.xml
RUN ~/miniconda3/bin/conda env create -f envs/environment_eclingo_reif.yml

# activate conda env, install eclingo and run benchmark
RUN echo "conda activate eclingo_reif" >> ~/.bashrc \
    && ~/miniconda3/bin/conda init bash \
    && . ~/.bashrc \
    && git clone https://github.com/jorgefandinno/eclingo.git \
    && cd eclingo/ \
    && pip install . \
    && cd .. \
    && nohup ./run.sh eclingo-no

# ENTRYPOINT ["bash"]