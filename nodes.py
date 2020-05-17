"""
    Note: You must add "nextcloud" in your ~/.ssh/config !
    see README
"""
import os

APT_DOCKER_PACKAGES = {
    # https://packages.ubuntu.com/focal/ubuntu-minimal
    'ubuntu-minimal',
    'openssh-server',
    'unattended-upgrades',
    'git',
    'htop',
    'nano',
    'docker.io',
    'docker-compose',
}


nodes = {
    'nextcloud': {
        'hostname': 'nextcloud',
        'bundles': [
            'journald', 'users', 'apt', 'purge_snap', 'nextcloud'
        ],
        'metadata': {
            'NEXTCLOUD_DOMAIN': os.environ.get('NEXTCLOUD_DOMAIN', 'localhost'),
            'apt-packages': APT_DOCKER_PACKAGES,
        }
    },
}
