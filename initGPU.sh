#!/usr/bin/env bash
cd nvidiacuda
chmod 777 *
./cuda-8.0.61.2_linux-run
cd ..
cd cudnn
tar -zxvf cudnn-8.0-linux-x64-v6.0.tgz

cd /root/nvidia/cudnn/cuda
cd include
cp cudnn.h /usr/local/cuda-8.0/include
cd ..
cd lib64
cp ./* /usr/local/cuda-8.0/lib64