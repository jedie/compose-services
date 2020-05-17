"""
    Install/uninstall packages via apt auto/manual
"""

global node  # bundlewrap.node.Node()


needed_packages = node.metadata['apt-packages']


def apt_mark_showmanual():
    result = node.run('apt-mark showmanual')
    assert result.return_code == 0
    output = result.stdout.decode('utf-8')
    packages = set(output.splitlines())
    return packages


manual_packages = apt_mark_showmanual()

to_install = needed_packages - manual_packages
to_uninstall = manual_packages - needed_packages


if to_install or to_uninstall:
    print('To install:', to_install)
    print('To uninstall:', to_uninstall)
    action_needed = '/bin/false'
else:
    print('\nNo install/uninstall needed, ok')
    action_needed = '/bin/true'


actions = {
    'apt-update': {
        'command': 'apt update',
        'expected_return_code': 0,
    },
    'mark-all-auto': {
        'command': 'apt-mark auto ".*"',
        'expected_return_code': 0,
        'needs': ['action:apt-update'],
        'unless': action_needed
    },
    'install-pakges': {
        'command': f'apt -y install {" ".join(needed_packages)}',
        'expected_return_code': 0,
        'needs': ['action:mark-all-auto'],
        'unless': action_needed
    },
    'upgrade': {
        'command': 'apt -y full-upgrade',
        'expected_return_code': 0,
        'needs': ['action:install-pakges'],
    },
    'autoremove': {
        'command': 'apt -y autoremove',
        'expected_return_code': 0,
        'needs': ['action:upgrade'],
        'unless': action_needed
    },
}

