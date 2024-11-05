FROM ubuntu:22.04

RUN apt update

WORKDIR /root/
RUN apt install -y wget
RUN apt install -y git
RUN apt -y install cmake
RUN apt install -y build-essential
RUN apt install -y software-properties-common

# clone the ezsmt repository
RUN git clone https://github.com/ylierler/ezsmt-uno.git --recurse-submodules

RUN wget https://archives.boost.io/release/1.79.0/source/boost_1_79_0.tar.bz2
# COPY boost_1_79_0.tar.bz2 /root/boost_1_79_0.tar.bz2

# install boost library
RUN mkdir boost \
    && cd boost \
    && tar --bzip2 -xf ../boost_1_79_0.tar.bz2 \
    && cd boost_1_79_0 \
    && ./bootstrap.sh \
    && ./b2 install

# build ezsmt
RUN cd ezsmt-uno \
    && mkdir build \
    && cd build \
    && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug .. \
    && cmake --build . 

# install gringo
RUN add-apt-repository ppa:potassco/stable \
    && apt update \
    && apt install -y gringo

# copy examples to image
COPY examples /root/examples/

# add tools and build directories to the PATH
RUN echo 'PATH="/root/ezsmt-uno/tools:$PATH"' >> ~/.bashrc \
    && echo 'PATH="/root/ezsmt-uno/build:$PATH"' >> ~/.bashrc \
    && . ~/.bashrc
