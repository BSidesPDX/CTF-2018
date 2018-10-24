#!/bin/sh

set -e

# create empty folder for workspace
rm -rf workspace
mkdir workspace
cp paper.png workspace/
cd workspace

# run generation script
cp ../arial.ttf .
python3 ../generate.py

# remove the stock paper photo
rm paper.png

# compress workspace
tar -czvf ../scans.tar.gz .
mv ../scans.tar.gz ../../distFiles/
rm -rf workspace

cd ..
