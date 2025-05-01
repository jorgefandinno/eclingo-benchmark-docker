FROM ubuntu:22.04

# setup environment variables
ENV solver_1=clingo-dl
ENV solver_2=ezsmt-z3-idl
ENV solver_3=ezsmt-yices-idl
ENV solver_4=ezsmt-cvc5-idl

ENV max_instances=3
ENV benchmark=routingMax,routingMin

ARG conda_env_file_path=envs/environment_ezsmt_clingodl.yml
ENV env_name=clingo-dl

# update and install required packages
RUN apt update
RUN apt install -y wget
RUN apt install -y git
RUN apt install -y cmake
RUN apt install -y build-essential
RUN apt install -y software-properties-common
RUN apt install -y python2
RUN apt install -y libnuma-dev

# set working directory
WORKDIR /root/

# download boost library package
RUN wget https://archives.boost.io/release/1.79.0/source/boost_1_79_0.tar.bz2

# install boost library
RUN mkdir boost \
    && cd boost \
    && tar --bzip2 -xf ../boost_1_79_0.tar.bz2 \
    && cd boost_1_79_0 \
    && ./bootstrap.sh \
    && ./b2 install

# install gringo
RUN add-apt-repository ppa:potassco/stable \
    && apt update \
    && apt install -y gringo

# clone the ezsmt repository
RUN git clone https://github.com/ylierler/ezsmt-uno.git --recurse-submodules

# build ezsmt
RUN cd ezsmt-uno \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug .. \
    && cmake --build . 

# add ezsmt tools and build directories to the PATH
ENV PATH=/root/ezsmt-uno/tools:$PATH
ENV PATH=/root/ezsmt-uno/build:$PATH

# install miniconda and initialize
RUN mkdir -p /root/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda3/miniconda.sh
RUN chmod +x ~/miniconda3/miniconda.sh
RUN bash /root/miniconda3/miniconda.sh -b -u -p /root/miniconda3
RUN rm -rf /root/miniconda3/miniconda.sh
RUN /root/miniconda3/bin/conda init bash

# add miniconda3 to the path
ENV PATH=/root/miniconda3/bin:$PATH

# copy benchmarking tool
COPY run-benchmark /root/run-benchmark/
WORKDIR /root/run-benchmark/

# create conda environment for ezsmt
RUN conda env create -f ${conda_env_file_path}

# copy setup bash file to image
COPY setup-ezsmt-clingodl.sh .


ENTRYPOINT ["/bin/bash", "-c"]
CMD ["./setup-ezsmt-clingodl.sh"]
