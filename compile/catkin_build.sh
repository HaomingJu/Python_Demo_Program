#!/usr/bin/env bash

# sudo apt install ccache distcc -y
# sudo systemctl restart distcc.service
# 配置文件 /etc/default/distcc
# 参考: https://github.com/kuka-isir/rtt_lwr/blob/rtt_lwr-2.0/docs/source/adv-tutos/ccache-distcc.rst

# export DISTCC_HOSTS="192.168.3.92/16 localhost/8"
# 设置服务器优先级以及最大核心数目

if [[ $1 ]]; then
    cd $1 && \
        echo `pwd`  && \
        export CCACHE_PREFIX="distcc"
        export CC="ccache gcc" CXX="ccache g++"
        export DISTCC_HOSTS="192.168.3.92/16 localhost/8"

        catkin config --install && \
        catkin build  -p32 -j32 --no-jobserver --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON && \
        cp build/$1/compile_commands.json src/$1/
fi
