FROM debian:bullseye
WORKDIR /workspace
RUN mkdir -p /workspace/lib
ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update && apt-get install -y --no-install-recommends curl git unzip xz-utils zip wget ssh sudo tar make g++ libtool autoconf automake zip unzip ca-certificates
RUN sudo mkdir -p /usr/local/share/ca-certificates/cacert.org
RUN wget -P /usr/local/share/ca-certificates/cacert.org http://www.cacert.org/certs/root.crt http://www.cacert.org/certs/class3.crt
RUN sudo update-ca-certificates
RUN git config --global http.sslCAinfo /etc/ssl/certs/ca-certificates.crt

# All commented parts are now done through CMakeFile to avoid having to build
# large libraries when trying to run docker-compose

# Install Bazel
#RUN wget https://github.com/bazelbuild/bazel/releases/download/5.0.0/bazel-5.0.0-installer-darwin-arm64.sh --no-check-certificate
#RUN chmod +x bazel-5.0.0-installer-darwin-arm64.sh && ./bazel-5.0.0-installer-darwin-arm64.sh --user
#ENV PATH="$PATH:$HOME/bin"

#WORKDIR /repos

# Install protobufs
#RUN git clone https://github.com/protocolbuffers/protobuf.git && cd protobuf && git submodule update --init --recursive && ./autogen.sh
#ENV LD_LIBRARY_PATH='/usr'
#RUN cd protobuf && ./configure --prefix=/usr && make -j$(nproc)
#WORKDIR /repos/protobuf
# RUN make check
#RUN make install && sudo ldconfig

# Install gRPC
#WORKDIR /repos
#ENV CC=/usr/bin/gcc-10
#RUN git clone https://github.com/grpc/grpc.git
#RUN apt install -y --no-install-recommends cmake
#RUN cd grpc && ~/bin/bazel build :all

# Configure, make
RUN apt-get install -y --reinstall postgresql libpq-dev build-essential gcc-10 g++-10 pkg-config
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 100
RUN update-alternatives --config gcc && update-alternatives --config g++

RUN apt-get install -y --no-install-recommends tmux cmake

# Install grpc, protobufs, and all dependencies using CMakeLists.txt
#COPY ./grpc-server /etc/grpc-server
#WORKDIR /etc/grpc-server
#RUN cmake .

# Install redis
WORKDIR /repos
RUN git clone https://github.com/redis/hiredis.git
RUN cd hiredis && make && make install
RUN git clone https://github.com/sewenew/redis-plus-plus.git && cd redis-plus-plus && mkdir build && cd build && cmake -DREDIS_PLUS_PLUS_CXX_STANDARD=14 ..
RUN cd redis-plus-plus/build && make && make install
