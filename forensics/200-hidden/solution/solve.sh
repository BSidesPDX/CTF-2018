#!/bin/sh

set -e

# create a workspace for the solution
rm -rf workspace
mkdir -p workspace

# copy wav file to the workspace
cp ../distFiles/output.wav ./workspace
cd ./workspace

# get tar file
steghide extract -sf ./output.wav -p "L0LWEAK" > /dev/null 2>&1
tar -xzf ./cooltar

# get the flag
chmod 777 .wow
strings .wow | grep "BSidesPDX"

