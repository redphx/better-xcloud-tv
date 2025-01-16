import hashlib
import json
import os
import re
import shutil
import subprocess

import requests

USERSCRIPT_URL = 'https://github.com/redphx/better-xcloud/raw/refs/heads/typescript/dist/better-xcloud.lite.user.js'
# USERSCRIPT_URL = 'https://github.com/redphx/better-xcloud/raw/main/better-xcloud.user.js'

# Read additional code
with open('src/js/additional.user.js', 'r') as file:
    addintional_code = file.read()

try:
    with open('src/js/local.user.js', 'r') as file:
        print('Use local userscript!')
        content = file.read()
except Exception:
    # Download userscript
    print('Downloading userscript...')
    content = requests.get(USERSCRIPT_URL).content.decode('UTF-8')

# Inject additional code
content = content.replace('/* ADDITIONAL CODE */', addintional_code)

# Get script's version
version_pattern = re.compile(r'SCRIPT_VERSION = "([^"]+)"')
match = version_pattern.search(content)
script_version = match.group(1)

# Remove "-beta" from version
script_version = script_version.replace('-beta', '')

print('Building version', script_version, '...')

# Remove 'tmp' dir
shutil.rmtree('tmp', ignore_errors=True)

# Copy files from 'src" to "tmp"
shutil.copytree('src', 'tmp')
# Delete "js" folder
shutil.rmtree('tmp/js', ignore_errors=True)
os.makedirs('tmp/webOSUserScripts', exist_ok=True)

# Write to userScript.js file
print('Saving to file...')
with open('tmp/webOSUserScripts/userScript.js', 'w') as file:
    file.write(content)

# Write to appinfo.json file
with open('tmp/appinfo.json', 'r') as file:
    info = file.read()
    info = info.replace('{{VERSION}}', script_version)

with open('tmp/appinfo.json', 'w') as file:
    file.write(info)


shutil.rmtree('dist', ignore_errors=True)
os.makedirs('dist')

# Build file
subprocess.run(['ares-package', '-n', '-o', 'dist', 'tmp'])
ipk_name = f'com.redphx.better-xcloud_{script_version}_all.ipk'

# Calculate SHA256 hash
with open(f'dist/{ipk_name}', 'rb', buffering=0) as fp:
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    while n := fp.readinto(mv):
        h.update(mv[:n])

    ipk_hash = h.hexdigest()

# Create manifest file
manifest = {
    'id': 'com.redphx.better-xcloud',
    'version': script_version,
    'type': 'web',
    'title': 'Better xCloud',
    'iconUri': 'https://raw.githubusercontent.com/redphx/better-xcloud-webos/main/assets/largeIcon.png',
    'sourceUrl': 'https://github.com/redphx/better-xcloud-webos',
    'rootRequired': False,
    'ipkUrl': ipk_name,
    'ipkHash':
    {
        'sha256': ipk_hash,
    }
}

# Save manifest to file
with open('dist/com.redphx.better-xcloud.manifest.json', 'w') as fp:
    json.dump(manifest, fp, indent=2)

print('Done')
