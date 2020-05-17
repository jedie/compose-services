# compose-services

## setup bundlewrap/server

prepare this:

* [install poetry](https://python-poetry.org/docs/#installation) e.g.:
```bash
~$ sudo apt install python3-pip
~$ pip3 install -U pip --user
~$ pip3 install -U poerty --user
```

* create virtualenv: `make install`
* copy `.env-example` to `.env` and setup values
* startup a server/node/vm with:
  * SSH access with Public-Key authentication
  * add "nextcloud" into your `~/.ssh/config`
  * setup "admin" user with `sudo` rights, without any password prompts
  
e.g.: `~/.ssh/config` entry for "nextcloud" node:

```
Host nextcloud
    HostName nextcloud.example.tld
    User admin
    IdentityFile ~/.ssh/id_rsa
    ControlPath ~/.ssh/ssh_multiplexing_%r@%h:%p
    ControlMaster auto
    ControlPersist 10m
```

Test SSH connection, e.g.:
```bash
compose-services$ ssh nextcloud id
uid=1000(admin) gid=1000(admin) groups=1000(admin),27(sudo)
```

To setup user "admin" on node "nextcloud", e.g.:
```bash
compose-services$ ssh root@nextcloud 'bash -s' < scripts/setup_user.sh "admin"
```

Check if sudo works without password input, e.g.:
```bash
compose-services$ ssh nextcloud sudo id
uid=0(root) gid=0(root) groups=0(root)
```

Check if bundlewrap can connect, too:
```bash
compose-services$ make nextcloud-uptime
poetry run bw -a run nextcloud "uptime"
› nextcloud   10:20:55 up 57 min,  0 users,  load average: 0.00, 0.00, 0.00
i ╭───────────┬─────────────┬────────╮
i │ node      │ return code │ time   │
i ├───────────┼─────────────┼────────┤
i │ nextcloud │           0 │ 0.809s │
i ╰───────────┴─────────────┴────────╯
```



## setup nextcloud

Setup server via bundlewrap:
```bash
compose-services$ make nextcloud-apply
```

Maybe after first "apply" a reboot may be needed for changes to take effect. (e.g.: setup docker usergroups)  

Update docker images:
```bash
compose-services$ make nextcloud-pull
ssh nextcloud 'docker-compose pull'
Pulling nextcloud-postgres ... done
Pulling nextcloud-redis    ... done
Pulling nextcloud          ... done
```

Start docker containers:
```bash
compose-services$ make nextcloud-up
ssh nextcloud 'docker-compose up -d'
Starting nextcloud-postgres ... done
Starting nextcloud-redis    ... done
Starting nextcloud          ... done
```
After a few seconds Nextcloud is available at http://nextcloud.example.tld from your host system.

To get the default admin password, run this:
```bash
compose-services$ make nextcloud-admin-password 
______________________________________________________________________
admin password is:
Foo-Bar-Foo-Bar-99
----------------------------------------------------------------------
```
Change the password on nextcloud web page!

Stop docker containers:
```bash
compose-services$ make nextcloud-stop 
ssh nextcloud 'docker-compose stop'
Stopping nextcloud          ... done
Stopping nextcloud-postgres ... done
Stopping nextcloud-redis    ... done
```



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


### setup unattended-upgrades

```bash
~$ sudo apt install unattended-upgrades
~$ sudo dpkg-reconfigure unattended-upgrades
~$ sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
```
* https://help.ubuntu.com/community/Security
* https://help.ubuntu.com/lts/serverguide/automatic-updates.html
* https://help.ubuntu.com/community/AutomaticSecurityUpdate
