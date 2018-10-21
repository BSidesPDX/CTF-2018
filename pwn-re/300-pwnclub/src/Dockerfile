# Use Ubuntu LTS 18.04
FROM ubuntu:18.04

# Add required files to /app and set working directory
WORKDIR /app
ADD . /app

# Install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends xinetd

# Setup file permissions
RUN adduser --disabled-password --gecos '' pwnclub
RUN chown root:pwnclub /app/pwnclub
RUN chown root:pwnclub /app/flag.txt
RUN chown root:pwnclub /app/pwnclub.c
RUN chown root:pwnclub /app/Dockerfile

RUN chmod 750 /app/pwnclub
RUN chmod 440 /app/flag.txt
RUN chmod 440 /app/pwnclub.c
RUN chmod 440 /app/Dockerfile

# Deploy the service file
COPY pwnclub.service /etc/xinetd.d/nodes

# Expose port 31337 and run xinetd
RUN echo "pwnclub 31337/tcp" >> /etc/services
EXPOSE 31337
CMD ["xinetd", "-dontfork"]
