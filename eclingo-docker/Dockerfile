# Download base image ubuntu 22.04
FROM ubuntu:22.04
# LABEL about the custom image
LABEL maintainer="kdhakal@unomaha.edu"
LABEL version="0.1"
LABEL description="This is a custom Docker Image for benchmarking and comparing solvers"
# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# setup all environment variables
ENV solver_1=eclingo
ENV solver_1_name=eclingo
ENV solver_2=eclingo
ENV solver_2_name=eclingo-old

ENV max_instances=2
ENV benchmark=yale

ENV conda_env_file_path_1=envs/environment_eclingo_reif.yml
ENV env_name_1=eclingo_reif
ENV conda_env_file_path_2=envs/environment_eclingo_old.yml
ENV env_name_2=eclingo_old

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

# add miniconda3 to the path
ENV PATH=/root/miniconda3/bin:$PATH

# Copy benchmark tool and create conda environment
COPY eclingo-benchmark /root/eclingo-benchmark/
WORKDIR /root/eclingo-benchmark/
# RUN sed -i 's/runsolver/eclingo/' run-benchmark.xml

# set bash (interactive) as the default shell
# SHELL ["/bin/bash", "-i", "-c"]

# create and activate eclingo_reif conda environment, install eclingo-new
RUN conda env create -f ${conda_env_file_path_1}
RUN eval "$(conda shell.bash hook)" \
    && conda activate ${env_name_1} \
    && git clone https://github.com/jorgefandinno/eclingo.git \
    && cd eclingo/ \
    && pip install .  

# create and activate eclingo_old conda environment, install eclingo-old
RUN conda env create -f ${conda_env_file_path_2}
RUN eval "$(conda shell.bash hook)" \
    && conda activate ${env_name_2} \
    && rm -r eclingo \
    && git clone https://github.com/potassco/eclingo.git \
    && cd eclingo/ \
    && git checkout tags/v0.2.1 \
    && pip install . 

# copy setup bash file to image
COPY setup.sh .

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["./setup.sh"]
