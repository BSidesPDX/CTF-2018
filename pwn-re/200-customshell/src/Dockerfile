# Use Ubuntu LTS 18.04
FROM ubuntu:18.04

# Add required files to /app and set working directory
WORKDIR /app
ADD . /app

# Install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends socat

# Setup file permissions
RUN adduser --disabled-password --gecos '' secureshell
RUN chown root:secureshell /app/secureshell
RUN chown root:secureshell /app/flag.txt
RUN chown root:secureshell /app/main.c
RUN chown root:secureshell /app/password.txt
RUN chown root:secureshell /app/Dockerfile

RUN chmod 750 /app/secureshell
RUN chmod 440 /app/flag.txt
RUN chmod 440 /app/main.c
RUN chmod 440 /app/password.txt
RUN chmod 440 /app/Dockerfile

# Expose port 7100 and use socat to redirect stdin/stdout to this port
EXPOSE 7100
CMD su secureshell -c "socat -T10 TCP-LISTEN:7100,reuseaddr,fork EXEC:/app/secureshell"
