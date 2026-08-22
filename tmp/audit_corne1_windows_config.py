#!/usr/bin/env python3
from pathlib import Path
import re, sys
root = Path('/Users/ryanparker/Documents/personal/code/corne1')
errors=[]
# Minimal build.yaml parser for the simple include matrix.
entries=[]; current=None
for line in (root/'build.yaml').read_text().splitlines():
    if re.match(r'\s*-\s+board:', line):
        if current: entries.append(current)
        current={'board': line.split(':',1)[1].strip()}
    elif current and ':' in line:
        k,v=line.strip().split(':',1)
        current[k]=v.strip()
if current: entries.append(current)
expected=[{'board':'nice_nano_v2','shield':'corne_left','artifact-name':'corne_left'}, {'board':'nice_nano_v2','shield':'corne_right','artifact-name':'corne_right'}, {'board':'nice_nano_v2','shield':'settings_reset','artifact-name':'settings_reset'}]
if entries != expected: errors.append(f'build matrix mismatch: {entries!r}')
# forbidden/stale settings
paths=[root/'build.yaml', root/'config/corne.conf', root/'config/corne.keymap', root/'config/corne.overlay']
all_text='\n'.join(p.read_text() for p in paths)
for forbidden in ['CONFIG_ZMK_STUDIO', 'studio-rpc-usb-uart', 'CONFIG_ZMK_RGB_UNDERGLOW=y', 'CONFIG_EC11=y', 'CONFIG_ZMK_DISPLAY=y', '&kp LGUI', '&kp LCMD', '&kp LG(']:
    if forbidden in all_text: errors.append(f'forbidden stale token present: {forbidden}')
# required settings/tokens
for required in ['CONFIG_BT_CTLR_TX_PWR_PLUS_8=y','CONFIG_BT_GATT_ENFORCE_SUBSCRIPTION=n','CONFIG_ZMK_SLEEP=y','CONFIG_ZMK_IDLE_SLEEP_TIMEOUT=900000','&bt BT_CLR','&bt BT_SEL 0','&bt BT_SEL 4','&kp LWIN']:
    if required not in all_text: errors.append(f'required token missing: {required}')
# keymap behavior count per layer should match 42-key transform
km=(root/'config/corne.keymap').read_text()
for layer in re.finditer(r'(default_layer|lower_layer|raise_layer)\s*\{.*?bindings\s*=\s*<(.*?)>;', km, re.S):
    count=len(re.findall(r'&(?:kp|mo|bt|trans)\b', layer.group(2)))
    if count != 42: errors.append(f'{layer.group(1)} has {count} bindings, expected 42')
if (root/'config/corne.dtsi').exists(): errors.append('config/corne.dtsi still exists')
print('audit-windows-zmk-config=' + ('fail' if errors else 'pass'))
for e in errors: print('ERROR:', e)
sys.exit(1 if errors else 0)
