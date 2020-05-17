files = {
    '/etc/systemd/journald.conf': {
        'mode': '0644',
        'owner': 'root',
        'group': 'root',
        'content_type': 'text',
        'encoding': 'utf-8',
        'source': 'journald.conf',
        'cascade_skip': False,
        'triggers': [
            'action:journald-reload',
        ],
    },
}
actions = {
    'journald-reload': {
        'command': 'systemctl restart systemd-journald',
        'triggered': True,
    }
}
