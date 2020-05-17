global node  # bundlewrap.node.Node()

NEXTCLOUD_DOMAIN = node.metadata['NEXTCLOUD_DOMAIN']
print(f' - NEXTCLOUD_DOMAIN: {NEXTCLOUD_DOMAIN!r}')

files = {
    '/home/admin/.dockerignoredocker-compose.yml': {
        'mode': '0644',
        'owner': 'admin',
        'group': 'admin',
        'content_type': 'mako',
        'encoding': 'utf-8',
        'source': 'docker-compose.yml',
        'context': {
            'NEXTCLOUD_DOMAIN': NEXTCLOUD_DOMAIN
        },
        'needs': [
            'bundle:apt',
            'bundle:users',
        ],
        'cascade_skip': False,
    },
    '/home/admin/docker-compose.yml': {
        'mode': '0644',
        'owner': 'admin',
        'group': 'admin',
        'content_type': 'mako',
        'encoding': 'utf-8',
        'source': 'docker-compose.yml',
        'context': {
            'NEXTCLOUD_DOMAIN': NEXTCLOUD_DOMAIN
        },
        'needs': [
            'bundle:apt',
            'bundle:users',
        ],
        'cascade_skip': False,
    },
    '/home/admin/traefik.yml': {
        'mode': '0644',
        'owner': 'admin',
        'group': 'admin',
        'content_type': 'mako',
        'encoding': 'utf-8',
        'source': 'traefik.yml',
        'context': {
            'NEXTCLOUD_DOMAIN': NEXTCLOUD_DOMAIN
        },
        'needs': [
            'bundle:apt',
            'bundle:users',
        ],
        'cascade_skip': False,
    },
}

actions = {
    'mkdir-docker-volumes': {
        'command': 'mkdir -p docker-volumes'
    },
    'touch-acme-json': {
        'command': 'touch ./docker-volumes/acme.json',
        'unless': 'test -f ./docker-volumes/acme.json',
        'needs': ['action:mkdir-docker-volumes'],
    },
    'chmod-acme-json': {
        'command': 'chmod 0600 ./docker-volumes/acme.json',
        'needs': ['action:touch-acme-json'],
    },
}
