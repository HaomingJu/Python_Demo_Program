#!/usr/bin/env bash

# sudo apt install ccache distcc -y
# 配置文件 /etc/default/distcc

if [[ $1 ]]; then
    cd $1 && \
        echo `pwd`  && \
        export CCACHE_PREFIX="distcc"
        export CC="ccache gcc" CXX="ccache g++"
        export DISTCC_HOSTS="gpu/16 localhost/8"
        export DISTCC_LOG="/var/log/trunk/distcc"

        catkin config --install && \
        catkin build  -p$(distcc -j) -j$(distcc -j) --no-jobserver --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON && \
        cp build/$1/compile_commands.json src/$1/
fi
