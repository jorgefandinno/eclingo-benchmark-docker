FROM ubuntu:22.04

# setup environment variables
ENV solver1=ezsmt
ENV solver2=clingcon
ENV max_instances=2
ENV benchmark=weighted-sequence

ENV conda_env_file_path=envs/environment_ezsmt.yml
ENV env_name=ezsmt

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

# add miniconda3 to the path
ENV PATH=/root/miniconda3/bin:$PATH

# create conda environment for ezsmt
RUN conda env create -f ${conda_env_file_path}

# copy setup bash file to image
COPY setup.sh .

# Adding below line escapes dollar sign with backward slash
# escape=`
RUN echo " \
\nconda activate ${env_name} \n\
./run.sh \${solver1} --max-instances=\${max_instances} --benchmark=\${benchmark} \n\
./run.sh \${solver2} --max-instances=\${max_instances} --benchmark=\${benchmark} \n\
python examine_output.py -s1 \${solver1} -s2 \${solver2} > log.txt \
" >> setup.sh

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["./setup.sh"]
