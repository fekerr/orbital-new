# Dockerfile
FROM ubuntu:20.04

# Suppress interactive prompts for apt
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install base packages essential for our environment.
# We no longer include ninja-build here since install_tools.sh handles it.
RUN apt-get update && \
    apt-get install -y python3 python3-pip git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the container working directory
WORKDIR /app

# Copy the entire repository into the container.
COPY . /app

# Ensure the install_tools.sh script is executable and run it.
RUN chmod +x install_tools.sh && \
    ./install_tools.sh

# Default command: open bash shell.
CMD ["bash"]
