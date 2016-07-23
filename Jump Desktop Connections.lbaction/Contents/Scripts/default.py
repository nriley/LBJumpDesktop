#!/usr/bin/env python
import glob, json, os, subprocess

jump_bundle_id = 'com.p5sys.jump.mac.viewer'

json_dir_path = subprocess.check_output([
	'/usr/bin/defaults', 'read', jump_bundle_id,
	'path where JSON .jump files are stored']).rstrip('\n')

items = []
for jump_path in glob.glob(os.path.join(json_dir_path, '*.jump')):
	jump = json.load(file(jump_path, 'r'))
	item = dict(((prop, jump[key] or '(none)')
				for key, prop in (('DisplayName', 'title'),
							      ('TcpHostName', 'label'))
		if key in jump))

	protocol = jump.get('ProtocolTypeCode')
	icon = jump.get('Icon')

	if not icon:
		icon = {0: 'com.p5sys.icons.windows.tintable',
				1: 'com.p5sys.icons.unknown.tintable',
				None: 'com.p5sys.icons.unknown.tintable'}[protocol]
		item['iconIsTemplate'] = True
	item['icon'] = '%s:%s' % (jump_bundle_id, icon)

	if protocol is not None:
		item['badge'] = {0: 'RDP', 1: 'VNC'}[protocol]

	item['path'] = jump_path
	item['subtitle'] = ''
	items.append(item)

print json.dumps(items)
