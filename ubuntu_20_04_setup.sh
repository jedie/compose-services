#!/bin/bash

# Setup a minimal Ubuntu 20.04 server
# Just install only really needed packages

set -e

PACKAGES=(
    # https://packages.ubuntu.com/focal/ubuntu-minimal
    ubuntu-minimal
    openssh-server
    unattended-upgrades
    git
    htop
    nano
    docker.io docker-compose
)

(
    set -x
    apt update
    { echo "---------------------------------------------------"; } 2>/dev/null
    # Mark all packages as 'Automatically installed'
    apt-mark auto '.*' > /dev/null;
    { echo "---------------------------------------------------"; } 2>/dev/null
    apt install "${PACKAGES[@]}"
    { echo "---------------------------------------------------"; } 2>/dev/null
    apt -y full-upgrade
    { echo "---------------------------------------------------"; } 2>/dev/null
    apt autoremove
    { echo "---------------------------------------------------"; } 2>/dev/null
)
