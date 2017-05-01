#!/bin/bash

#
# This script configures a Windows Subsystem for Linux (WSL) environment for
# running tests on BitFunnel, Partitioned Elias-Fano, mg4j, and Lucene.
#
# Before running be sure to set the following environment variables:
#   EMAIL: the email address used to configure the ssh key.
#

# Install tools
sudo apt-get install gcc
sudo apt-get install g++
sudo apt-get install cmake
sudo apt-get install git

# Set up ssh key for github.
ssh-keygen -t rsa -b 4096 -C "$EMAIL"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub
echo -n Add the above ssh key to github and then press enter to continue.
read text

# Setup partitioned_elias_fano
git clone --recursive git@github.com:BitFunnel/partitioned_elias_fano.git
cd partitioned_elias_fano/
cmake . -DCMAKE_BUILD_TYPE=Release
make
bin/create_freq_index opt /mnt/d/temp/PartitionedEliasFano/export ~/data/ten.index.opt
bin/Runner opt \
           ~/data/ten.index.opt \
            /mnt/d/temp/PartitionedEliasFano/export-filtered-ints.txt \
            8 \
            ~/data/out.csv

