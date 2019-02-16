#!/usr/bin/env python
import glob
import json
import os
import subprocess

jump_bundle_id = 'com.p5sys.jump.mac.viewer'

json_dir_path = subprocess.check_output([
    '/usr/bin/defaults', 'read', jump_bundle_id,
    'path where JSON .jump files are stored']).rstrip('\n')

unknown_icon = 'com.p5sys.icons.unknown.tintable'
ostype_icon = {0: unknown_icon,  # redundant, for completeness
               1: 'com.p5sys.icons.windows.tintable',
               2: 'com.p5sys.icons.mac.tintable'}

protocol_name = {0: 'RDP', 1: 'VNC', 2: 'Fluid'}

items = []
for jump_path in glob.glob(os.path.join(json_dir_path, '*.jump')):
    jump = json.load(file(jump_path, 'r'))

    item = dict(((prop, jump[key] or default)
                for key, prop, default in (('DisplayName', 'title', '(none)'),
                                           ('TcpHostName', 'label', ''))
                 if key in jump))

    protocol = jump.get('ProtocolTypeCode')
    ostype = jump.get('OsTypeCode')
    icon = jump.get('Icon')

    if not icon:
        icon = ostype_icon.get(ostype, unknown_icon)
        item['iconIsTemplate'] = True

    item['icon'] = '%s:%s' % (jump_bundle_id, icon)

    badge = protocol_name.get(protocol, None)
    if badge is not None:
        item['badge'] = badge

    item['path'] = jump_path
    item['subtitle'] = ''
    items.append(item)

print json.dumps(items)
