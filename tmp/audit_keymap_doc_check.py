#!/usr/bin/env python3
from pathlib import Path

keymap = Path('config/corne.keymap').read_text().splitlines()
keymap_line = next((i for i,l in enumerate(keymap,1) if '&kp LCTRL  &trans  &kp LSHFT' in l), None)
keymap_comment = next((i for i,l in enumerate(keymap,1) if '| CTRL|     | SHFT|' in l), None)
keymap_value = keymap[keymap_line-1].strip() if keymap_line else '<not found>'

keymap_doc = Path('KEYMAP.md').read_text().splitlines()
doc_transparent_line = next((i for i,l in enumerate(keymap_doc,1) if 'remaining `LWR` thumb positions are `transparent`' in l), None)
doc_thumb_line = next((i for i,l in enumerate(keymap_doc,1) if '| Thumbs | `&kp LCTRL` `&trans` `&trans`' in l), None)

print(f'config/corne.keymap:{keymap_line}: {keymap_value}')
print(f'config/corne.keymap:{keymap_comment}: {keymap[keymap_comment-1].strip() if keymap_comment else "<comment not found>"}')
print(f'KEYMAP.md:{doc_transparent_line}: {keymap_doc[doc_transparent_line-1] if doc_transparent_line else "<not found>"}')
print(f'KEYMAP.md:{doc_thumb_line}: {keymap_doc[doc_thumb_line-1] if doc_thumb_line else "<not found>"}')

if keymap_line and doc_transparent_line and doc_thumb_line:
    raise SystemExit('Mismatch confirmed: keymap has LWR left-inner thumb &kp LSHFT while KEYMAP documents transparent LWR non-left-outer thumbs.')
