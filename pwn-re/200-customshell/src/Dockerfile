# Use Ubuntu LTS 18.04
FROM ubuntu:18.04

# Add required files to /app and set working directory
WORKDIR /app
ADD . /app

# Install dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends socat

# Make sure binary is executable
RUN chmod 750 /app/secureshell

# Expose port 7100 and use socat to redirect stdin/stdout to this port
EXPOSE 7100
CMD socat -T10 TCP-LISTEN:7100,reuseaddr,fork EXEC:/app/secureshell
