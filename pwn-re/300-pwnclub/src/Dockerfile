# Use Ubuntu LTS 18.04
FROM ubuntu:18.04

# Add required files to /app and set working directory
WORKDIR /app
ADD . /app

# Install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends socat

# Setup file permissions
RUN adduser --disabled-password --gecos '' pwnclub
RUN chown root:pwnclub /app/pwnclub
RUN chown root:pwnclub /app/flag.txt
RUN chown root:pwnclub /app/main.c
RUN chown root:pwnclub /app/Dockerfile

RUN chmod 750 /app/pwnclub
RUN chmod 440 /app/flag.txt
RUN chmod 440 /app/main.c
RUN chmod 440 /app/Dockerfile

# Expose port 31337 and use socat to redirect stdin/stdout to this port
EXPOSE 31337
CMD su pwnclub -c "socat -T10 TCP-LISTEN:31337,reuseaddr,fork EXEC:/app/pwnclub"
