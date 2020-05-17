global node  # bundlewrap.node.Node()

"""
    FIXME: Will need a restart of a virtual machine.
"""

groups = {
    'sudo': {},
    'docker': {},
}

actions = {
    'add-admin-to-docker': {
        'command': 'sudo usermod -aG docker admin',
        'expected_return_code': 0,
    },
}