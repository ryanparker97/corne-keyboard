# macOS data engineering / DevOps keymap

This 42-key Corne layout targets data engineering and DevOps work on macOS: SQL, Python, shell, YAML/JSON, Terraform/HCL, Docker, Kubernetes, Vim, and stock tmux. It intentionally uses **no home-row mods, mod-taps, layer-taps, sticky modifiers, tap dance, or combos**. Letters are ordinary keys; modifiers and layer keys always do exactly one thing.

There is no objectively best keymap. This one favors familiar QWERTY positions, mnemonic navigation, short finger travel, and a small number of focused layers.

## Base thumb keys

```text
left hand                 right hand
OPTION RAISE  COMMAND   |  SPACE  LOWER  ENTER
```

- Hold **RAISE** for data, infrastructure, and shell symbols.
- Hold **LOWER** for numbers, navigation, terminal prefixes, and function keys.
- Hold **RAISE + LOWER** for system controls.

## Base — `Base`

```text
ESC   Q     W     E     R     T   |  Y     U     I     O     P     BSPC
TAB   A     S     D     F     G   |  H     J     K     L     ;     '
SHIFT Z     X     C     V     B   |  N     M     ,     .     /     CONTROL
                OPT   RAISE  CMD  |  SPACE  LOWER  ENTER
```

Option and Command are on Base-layer thumbs for macOS shortcuts. Control and Shift remain dedicated edge keys. The left outer thumb becomes Control on the other layers, keeping layered navigation and terminal chords accessible. Nothing changes meaning based on tap duration.

## Lower — `Nav/Num`

```text
`     1     2     3     4     5   |  6     7     8     9     0     DEL
VIM   CTRL  OPT   CMD   SHIFT TMUX|  LEFT  DOWN  UP    RIGHT PGDN  PGUP
F1    F2    F3    F4    F5    F6  |  F7    F8    F9    F10   F11   F12
                CTRL  RAISE  CMD  |  SPACE  LOWER  ENTER
```

The navigation row deliberately puts arrows on physical **H/J/K/L**. The left-hand modifiers are ordinary held keys, so macOS editing stays ergonomic and predictable:

- `LOWER + Option + Left/Right`: move by word.
- `LOWER + Command + Left/Right`: move to the start/end of a line.
- `LOWER + Command + Up/Down`: move to the start/end of a document.
- Add `LOWER + Shift` to extend the selection.

`VIM` emits and releases `Ctrl-W`; while still holding Lower, tap an arrow on H/J/K/L to move between Vim windows. `TMUX` emits and releases stock `Ctrl-B`; tap a Lower-layer arrow next to move between tmux panes. Releasing Control inside each prefix macro avoids accidentally sending `Ctrl-Arrow` as the follow-up command.

## Raise — `Symbols`

```text
~     !     @     #     $     %   |  ^     &     *     (     )     ?
-     CTRL  OPT   CMD   SHIFT =   |  [     {     :     |     }     ]
\      '     "     _     +     `   |  <     >     ,     .     /     ;
                CTRL  RAISE  CMD  |  SPACE  LOWER  ENTER
```

The top row mirrors the normal shifted number order, reducing memorization. The right home row groups Python/data structures and YAML operators as `[ { : | } ]`. Python's underscore, colon, both quotes, parentheses, decorators (`@`), comments (`#`), f-string braces, arithmetic operators, comparisons, comma, and period are all direct. Backtick, `-`, `=`, `$`, slash, pipe, and backslash remain direct for SQL, shell, and infrastructure code. Comma, period, and slash stay in their Base positions; semicolon remains direct on the outer bottom key, while `<` and `>` move inward for comparisons and `->` annotations.

### Workflow rationale

| Workload | Prioritized syntax |
| --- | --- |
| Python, PySpark, Airflow | `_`, `:`, quotes, `()`, `[]`, `{}`, `@`, `#`, `*`, `/`, comparisons, `->` |
| SQL and warehouses | `()`, quotes, `_`, `=`, comma, period, comparison operators, semicolon |
| YAML, Kubernetes, Ansible | `-`, `:`, `#`, `|`, `>`, quotes, `[]`, `{}` |
| JSON and Terraform/HCL | `{}`, `[]`, `=`, quotes, `.`, `_`, `$` |
| Shell, Docker, kubectl | `-`, `_`, `/`, `=`, `$`, `#`, backslash, pipe, `&`, `<`, `>`, backtick |

The keymap intentionally does not type command names or deployment operations for you. Explicit commands remain safer across clusters, accounts, shells, SQL engines, and changing CLI versions.

## Adjust — `System`

```text
BOOT  BT1   BT2   BT3   BT4   BT5 |  CAP   CWORD CAPS  SPOT  APP   LOCK
BTCLR PREV  PLAY  NEXT  MUTE  VOL- |  TOG   FX+   HUE+  SAT+  BRI+  SPD+
RESET DISP- DISP+ USB   BLE   VOL+ |  OUT   FX-   HUE-  SAT-  BRI-  SPD-
                CTRL  RAISE  CMD  |  SPACE  LOWER  ENTER
```

- `CAP`: macOS **Shift-Command-5** capture UI for screenshots and recordings.
- `CWORD`: Caps Word, convenient for SQL keywords such as `SELECT` and constants such as `MAX_RETRIES`; it stops automatically on normal word-breaking input.
- `CAPS`: traditional Caps Lock remains available.
- `SPOT`, `APP`, `LOCK`: Spotlight, app switcher, and screen lock.
- Bluetooth, USB/BLE output, media, brightness, RGB, bootloader, and reset controls are retained.

## Build and flash

Run the repository's **Build ZMK firmware** GitHub Actions workflow (or push a branch that changes `config/**`). Download the left and right firmware artifacts and flash each artifact to its matching half.

## Research basis

The layout adapts ideas rather than copying one keymap wholesale:

- [Miryoku reference](https://github.com/manna-harbour/miryoku/tree/master/docs/reference): thumb layers, focused layer roles, aligned number/symbol positions, home-position navigation, and plain modifiers on layers.
- [Designing a Symbol Layer](https://getreuer.info/posts/keyboards/symbol-layer/index.html): language-specific frequency, related symbol grouping, mnemonic placement, and comfortable symbol sequences.
- [Python lexical analysis](https://docs.python.org/3/reference/lexical_analysis.html): underscores, comments, strings, f-string braces and colons, operators, delimiters, decorators, and annotations.
- [PEP 8](https://peps.python.org/pep-0008/): underscore-heavy naming, delimiters, trailing commas, comparisons, annotations, and operator spacing.
- [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/): dashes and colons for collections, `#` comments, `|`/`>` block scalars, quotes, brackets, and braces.
- [Terraform configuration syntax](https://developer.hashicorp.com/terraform/language/syntax/configuration): `=` arguments, brace-delimited blocks, underscores/hyphens, quotes, and `#` comments.
- [PostgreSQL lexical structure](https://www.postgresql.org/docs/current/sql-syntax-lexical.html): quotes, identifiers, operators, parentheses, brackets, comma, period, and semicolon.
- [Bash definitions](https://www.gnu.org/software/bash/manual/html_node/Definitions.html): shell control operators, metacharacters, identifiers, and pipelines.
- [kubectl Quick Reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/) and [Docker CLI reference](https://docs.docker.com/reference/cli/docker/): real-world use of flags, assignments, paths, YAML/JSON, templates, pipes, and redirection.
- [niqodea's Corne layout](https://github.com/niqodea/crkbd): QWERTY familiarity, Vim mnemonics, thumb layers, and a compact four-layer model.
- [Callum's no-mod-tap keymap](https://github.com/callum-oakley/qmk_firmware/tree/master/users/callum): avoiding tap/hold timing ambiguity on small keyboards.
- [ZMK v0.3 keymaps](https://v0-3-branch.zmk.dev/docs/keymaps) and [macros](https://v0-3-branch.zmk.dev/docs/behaviors/macros): the pinned firmware's layer and macro behavior.
- [Apple keyboard shortcuts](https://support.apple.com/en-us/102650): macOS text navigation, selection, app switching, screen lock, and Shift-Command-5.
- [tmux Getting Started](https://github.com/tmux/tmux/wiki/Getting-Started): stock `Ctrl-B` prefix, release-before-command semantics, and arrow-key pane selection.
- [Vim windows help](https://vimhelp.org/windows.txt.html): `Ctrl-W` window commands and directional navigation.
