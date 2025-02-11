FROM ubuntu:22.04

RUN apt update

RUN apt install -y wget
RUN apt install -y git
RUN apt install -y cmake
RUN apt install -y build-essential
RUN apt install -y software-properties-common
RUN apt install -y python2
RUN apt install -y libnuma-dev

WORKDIR /root/

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

# add tools and build directories to the PATH
RUN echo 'PATH="/root/ezsmt-uno/tools:$PATH"' >> ~/.bashrc \
    && echo 'PATH="/root/ezsmt-uno/build:$PATH"' >> ~/.bashrc \
    && . ~/.bashrc

# copy benchmarking tool
COPY eclingo-benchmark /root/eclingo-benchmark/
WORKDIR /root/eclingo-benchmark/

# install miniconda and initialize
RUN mkdir -p /root/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /root/miniconda3/miniconda.sh
RUN chmod +x ~/miniconda3/miniconda.sh
RUN bash /root/miniconda3/miniconda.sh -b -u -p /root/miniconda3
RUN rm -rf /root/miniconda3/miniconda.sh
RUN /root/miniconda3/bin/conda init bash

# create conda environment for ezsmt
RUN /root/miniconda3/bin/conda env create -f envs/environment_ezsmt.yml

# activate conda env, run benchmark tool, and compare the outputs
RUN echo "conda activate ezsmt" >> /root/.bashrc \
    && . /root/.bashrc \
    && ./run.sh ezsmt --max-instances=2 --benchmark=weighted-sequence > log.txt \
    && ./run.sh clingcon --max-instances=2 --benchmark=weighted-sequence >> log.txt \
    && python examine_output.py -s1 ezsmt -s2 clingcon -l 1 >> log.txt
