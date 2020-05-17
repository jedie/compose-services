global node  # bundlewrap.node.Node()


def get_snap_mountpoints():
    result = node.run('mount')
    assert result.return_code == 0
    output = result.stdout.decode('utf-8')
    lines = [line for line in output.splitlines() if '/snap/' in line]
    mount_points = [line.split(' ')[2] for line in lines]
    return mount_points


actions = {}
for no, mount_point in enumerate(get_snap_mountpoints()):
    actions[f'unmount-{no}'] = {
        'command': f'umount {mount_point}',
        'expected_return_code': 0,
    }

if actions:
    needs = [f'action:{key}' for key in actions.keys()]
else:
    needs = []

actions['purge_snap'] = {
    'command': 'sudo rm -Rf /snap/',
    'expected_return_code': 0,
    'unless': 'test ! -x /snap/',
    'needs': needs,
}
