# Use Ubuntu LTS 18.04
FROM ubuntu:18.04

# Add required files to /app and set working directory
WORKDIR /app
ADD . /app

# Install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends xinetd

# Setup file permissions
RUN adduser --disabled-password --gecos '' secureshell
RUN chown root:secureshell /app/secureshell
RUN chown root:secureshell /app/flag.txt
RUN chown root:secureshell /app/secureshell.c
RUN chown root:secureshell /app/password.txt
RUN chown root:secureshell /app/Dockerfile

RUN chmod 750 /app/secureshell
RUN chmod 440 /app/flag.txt
RUN chmod 440 /app/secureshell.c
RUN chmod 440 /app/password.txt
RUN chmod 440 /app/Dockerfile

# Deploy the service file
COPY secureshell.service /etc/xinetd.d/nodes

# Expose port 7100 and run xinetd
RUN echo "secureshell 7100/tcp" >> /etc/services
EXPOSE 7100
CMD ["xinetd", "-dontfork"]
