# compose-services
Docker compose services

1. make base setup and install docker / docker-compose (see below)
2. do steps in "setup <service>" sections

## setup nextcloud

e.g.:

```bash
# install htpasswd:
~$ sudo apt install apache2-utils

~$ git clone https://github.com/jedie/compose-services.git
~$ cd compose-services/nextcloud
compose-services/nextcloud$ cp example-env .env

# Generate basic auth credentials for traefik:
compose-services/nextcloud$ htpasswd .basic_auth admin

# Start containers
compose-services/nextcloud$ make up
compose-services/nextcloud$ make
help                 List all commands
pull                 Pull service images
up                   Start containers in the background and display logs
stop                 Stop containers
restart              Restart containers by stop&start and display logs
logs                 Display container logs
```
After a few seconds Nextcloud is available at http://nextcloud.example.tld from your host system.


## base setup

```bash
~# nano /etc/ssh/sshd_config
```

Change e.g.:
```bash
Port xxxx
PermitRootLogin no
PasswordAuthentication no
```

```bash
~# service ssh restart
~# journalctl -f -u ssh
```

add a normal user:
```bash
~# export USERNAME=example
~# adduser --disabled-password --home=/home/${USERNAME} ${USERNAME}
~# usermod -aG sudo ${USERNAME}
~# mkdir -p /home/${USERNAME}/.ssh
~# cp /root/.ssh/authorized_keys /home/${USERNAME}/.ssh/
~# chown -Rfc ${USERNAME}.${USERNAME} /home/${USERNAME}/
~# echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL">/etc/sudoers.d/${USERNAME}
```
...login via SSH as new normal user...


### setup unattended-upgrades

```bash
~$ sudo apt install unattended-upgrades
~$ sudo dpkg-reconfigure unattended-upgrades
~$ sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
```
* https://help.ubuntu.com/community/Security
* https://help.ubuntu.com/lts/serverguide/automatic-updates.html
* https://help.ubuntu.com/community/AutomaticSecurityUpdate


### setup journald

e.g.: `sudo nano /etc/systemd/journald.conf`
```
[Journal]
Storage=persistent
Compress=yes
SplitMode=uid
RateLimitInterval=0
RateLimitBurst=0
ForwardToSyslog=no
ForwardToKMsg=no
ForwardToConsole=no
ForwardToWall=no
RuntimeMaxFileSize=256M
SystemMaxFileSize=256M
```

```bash
# display disk usage:
$ journalctl --disk-usage
$ du -h /var/log/

Status of journald:
$ systemctl status systemd-journald

# Delete old journald entries:
$ sudo journalctl --vacuum-size=1G
$ sudo journalctl --vacuum-time=1years
```

* https://www.freedesktop.org/software/systemd/man/journald.conf.html


### setup docker / docker-compose

see: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
or just:
```bash
$ sudo apt install docker.io docker-compose
$ sudo usermod -aG docker ${USER}
$ sudo systemctl status docker
$ docker --version
```


### docker tips

Remove unused containers, networks, images (until one week):
```
docker system prune --force --all --filter until=168h
```