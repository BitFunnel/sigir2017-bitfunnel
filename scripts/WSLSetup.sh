#!/bin/bash

#
# This script configures a Windows Subsystem for Linux (WSL) environment for
# running tests on BitFunnel, Partitioned Elias-Fano, mg4j, and Lucene.
#
# The purpose of this script is to document the steps needed to configure
# the environment. It has not been tested end-to-end on a clean machine.
#
# Before running be sure to set the following environment variables:
#   EMAIL: the email address used to configure git and the github ssh key.
#   FULLNAME: for configuring git's user.name field.
#

# C++ related
sudo apt-get install gcc
sudo apt-get install g++
sudo apt-get install cmake
sudo apt-get install emacs24

# Install never version of gcc, g++
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc-5 g++-5
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60 --slave /usr/bin/g++ g++ /usr/bin/g++-5

# Java + Maven related
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
sudo apt-get install maven

# Install and configure git
sudo apt-get install git
git config --global user.email "$EMAIL"
git config --global user.name "$FULLNAME"

# Set up ssh key for github.
ssh-keygen -t rsa -b 4096 -C "$EMAIL"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub
echo -n "Add the above ssh key to github and then press enter to continue."
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

