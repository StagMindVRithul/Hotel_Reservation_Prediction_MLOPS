# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install prerequisites for Docker and Docker installation script
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    apt-get clean

# Add Jenkins user to the Docker group (create if it doesn't exist)
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Optionally, create the Docker directory for Docker-in-Docker, but this step is only needed if you're using DinD
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Mount Docker socket (if running Docker on the host)
VOLUME /var/run/docker.sock:/var/run/docker.sock

# Switch back to the Jenkins user
USER jenkins
