# Dockerfile
FROM ubuntu:20.04

# Suppress interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install required packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip ninja-build git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory inside container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Ensure the install_tools.sh script is executable and run it
RUN chmod +x install_tools.sh && \
    ./install_tools.sh

# Set the default command to bash
CMD ["bash"]
