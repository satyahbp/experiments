#!/bin/sh

echo "Removing any existing docker instance..."
sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-doc docker-buildx podman-docker containerd runc | cut -f1)

# Add Docker's official GPG key:
echo "Adding docker GPG key..."
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

# installing latest version
echo "Installing docker..."
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Check if the Docker daemon is responding
echo "Checking docker installation..."
if docker info > /dev/null 2>&1; then
    echo "Docker is already running."
else
    echo "Docker is not running. Starting Docker..."

    # Start Docker using systemd (most Linux distros)
    if command -v systemctl > /dev/null 2>&1; then
        sudo systemctl start docker
    # Fall back to the service command for older systems
    elif command -v service > /dev/null 2>&1; then
        sudo service docker start
    else
        echo "Could not find systemctl or service. Please start Docker manually."
        exit 1
    fi

    # Give the daemon a few seconds to come up, then verify
    sleep 3
    if docker info > /dev/null 2>&1; then
        echo "Docker started successfully."
    else
        echo "Failed to start Docker. Check the logs with: journalctl -u docker"
        exit 1
    fi
fi
