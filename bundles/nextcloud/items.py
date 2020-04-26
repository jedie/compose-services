global node  # bundlewrap.node.Node()

NEXTCLOUD_DOMAIN = node.metadata['NEXTCLOUD_DOMAIN']
print(f' - NEXTCLOUD_DOMAIN: {NEXTCLOUD_DOMAIN!r}')


files = {
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
}

# actions = {
#     'pull': {
#         'command': 'docker-compose pull',
#         'expected_return_code': 0,
#         'needs': ['file:'],
#         'cascade_skip': False,
#     },
#     'up': {
#         'command': 'docker-compose up -d',
#         'expected_return_code': 0,
#         'needs': ['action:pull'],
#         'cascade_skip': False,
#     },
# }
