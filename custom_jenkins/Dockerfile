# Use the official Jenkins LTS base image
FROM jenkins/jenkins:lts

# Switch to root user to install packages
USER root

# Install Python 3.13.3 and other utilities
RUN apt-get update && \
    apt-get install -y wget build-essential zlib1g-dev libssl-dev libncurses5-dev libffi-dev libsqlite3-dev libbz2-dev libreadline-dev liblzma-dev libgdbm-dev libnss3-dev libxml2-dev libxmlsec1-dev && \
    cd /usr/src && \
    wget https://www.python.org/ftp/python/3.13.3/Python-3.13.3.tgz && \
    tar xzf Python-3.13.3.tgz && \
    cd Python-3.13.3 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    ln -s /usr/local/bin/python3.13 /usr/bin/python3.13 && \
    ln -s /usr/local/bin/pip3.13 /usr/bin/pip3.13 && \
    rm -rf /usr/src/Python-3.13.3*

# Verify Python version
RUN python3.13 --version && pip3.13 --version

# Setup a virtual environment (optional but ready)
RUN python3.13 -m venv /opt/jenkins-venv

# Fix permissions and switch back to Jenkins user
RUN chown -R jenkins:jenkins /opt/jenkins-venv
USER jenkins

# Default Jenkins ports
EXPOSE 8080 50000
