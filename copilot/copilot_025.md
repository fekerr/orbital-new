<build-environment> #003:

---

### Raw Prompt Input
```
Begin building a target in the ninja build for "install tools" or a script if that's easier. If the script is less than 15 lines, use bash. Probably use python though.

pip3 install PyYAML

Keep in mind we'll need to do this in the docker container anyway. So start building that docker file.
```

---

### Restated Input Prompt
You want to set up a build target or a standalone script that installs required tools (in this case, PyYAML via pip3). This target/script should be invoked via Ninja (or via a simple bash script if it’s short enough). Since we’ll eventually run everything inside a Docker container, we are also preparing a Dockerfile that sets up the build environment in a reproducible way.

We'll provide:
1. A small Bash script (less than 15 lines) named `install_tools.sh` that installs PyYAML.
2. A snippet for a Ninja build target that calls this script.
3. A Dockerfile that uses this script to initialize the build environment.

---

### Detailed Response

#### 1. `install_tools.sh`

This simple Bash script installs PyYAML using pip3. It’s only a few lines long, making it easy to maintain.

```bash
#!/bin/bash
# install_tools.sh
# This script installs the required Python packages for the project.
# Here, we upgrade pip and install PyYAML.

set -e  # Stop execution if any command fails

pip3 install --upgrade pip
pip3 install PyYAML
```

*Make sure the script is executable:*

```bash
chmod +x install_tools.sh
```

---

#### 2. Ninja Build Target

Below is a snippet you can add to your `build.ninja` file. This target will run the `install_tools.sh` script to install necessary tools.

```ninja
# build.ninja

# Define a rule to install required tools by running the install_tools.sh script
rule install_tools
  command = ./install_tools.sh
  description = Installing required Python packages (PyYAML)

# Create a phony build target for installing tools that depends on the script.
build install_tools: phony install_tools.sh
```

*Explanation:*
- The `rule install_tools` runs the bash script.
- The target `install_tools` is marked as phony, meaning it will be executed on demand (and isn’t tied to a specific file output).

---

#### 3. Dockerfile

This Dockerfile prepares a reproducible build environment by installing required operating system packages, Python 3, pip, Ninja, and then runs the `install_tools.sh` script to install Python packages.

```dockerfile
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
```

*Explanation:*
- **FROM ubuntu:20.04**: Base image; you can adjust the version as needed.
- **ENV DEBIAN_FRONTEND=noninteractive**: Prevents interactive prompts.
- **RUN apt-get update ...**: Installs Python3, pip, Ninja, and Git.
- **WORKDIR /app** and **COPY . /app**: Set the container’s working directory and copy the project files.
- **RUN chmod +x install_tools.sh && ./install_tools.sh**: Makes sure the installer script is executable and then runs it to install PyYAML.
- **CMD ["bash"]**: Opens a bash shell by default when the container runs.

---

### Summary & Next Steps

- **Wrapper Script:**  
  The `install_tools.sh` script (only 5 lines) installs PyYAML using pip3.
  
- **Ninja Target:**  
  The snippet in `build.ninja` defines a target (`install_tools`) that runs the script.
  
- **Docker Environment:**  
  The Dockerfile sets up a containerized environment that installs the OS-level dependencies and executes the `install_tools.sh` to install Python dependencies.

**Standard Approaches:**  
- Using Docker ensures consistent build environments.
- Ninja targets allow you to encapsulate build steps in a fast and incremental build system.
- Wrapper scripts (in Bash or Python) keep simple tasks modular and easily testable.

You can now commit these files to your repository and document this process in your `BUILD.md` or README, explaining how to build the Docker image and run the build tools.

Would you like to proceed with further modifications or additional features?
