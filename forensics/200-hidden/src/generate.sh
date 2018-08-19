#!/bin/sh

set -e

# define variables
flag="$(cat flag)"
teaser='the flag must be somewhere around here, right?'
message='Progress, but where is the key hidden?'

# create the workspace
rm -rf workspace
mkdir -p workspace
cp ./input.wav ./workspace/output.wav
cd ./workspace

# create files
len=${#flag}
backspaces="$(head -c $len < /dev/zero | tr '\0' '\b')"
echo "$flag$backspaces$teaser" > .wow
chmod 000 .wow
echo "$teaser" > message

# needs root because .wow file has 000 permissions
sudo tar -czf cooltar .wow

# embed files
steghide embed -cf output.wav -ef cooltar -p "L0LWEAK" > /dev/null 2>&1
steghide embed -cf output.wav -ef message -p "" > /dev/null 2>&1

# now, your file is in ./workspace/output.wav
echo "./workspace/output.wav";
