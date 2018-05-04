#!/usr/bin/env bash
cd /root/nvidia/cudnn/
cd include
cp cudnn.h /usr/local/cuda-8.0/include
cd ..
cd lib64
cp ./* /usr/local/cuda-8.0/lib64