#!/usr/bin/env bash

set -ex

export USERNAME=${1}

sudo adduser --disabled-password --gecos "" --home=/home/${USERNAME} ${USERNAME}
sudo usermod -aG sudo ${USERNAME}
sudo mkdir -p /home/${USERNAME}/.ssh
sudo cp /root/.ssh/authorized_keys /home/${USERNAME}/.ssh/
sudo chown -Rfc ${USERNAME}.${USERNAME} /home/${USERNAME}/
sudo echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL">/etc/sudoers.d/${USERNAME}