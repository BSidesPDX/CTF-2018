# Forensics 300 Creation

To create the forensics 300 problem, simply execute `sh generate.sh` in the `src` directory. A file named `scans.tar.gz` will be assembled, compressed, and placed in the `distFiles` directory.

The generation script does the following to generate each image, before compressing the directory containing the images:
1. Create a randomly generated image of paper
2. Generate the dot matrix with a random serial code (or the flag file)
3. Draw it as many times as it fits with 1/2" padding between the matrices, and a 1/2" margin around the paper
4. Save to file
