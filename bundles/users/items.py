global node  # bundlewrap.node.Node()

groups = {
    'sudo': {},
    'docker': {},
}

users = {
    'admin': {
        'full_name': 'bundlewrap',
        'groups': ['sudo', 'docker'],
        'home': '/home/admin/',
        'password_hash': '',
        'shell': '/bin/bash',
        # 'uid': 4747,
        # 'gid': 2342,
    },
}
