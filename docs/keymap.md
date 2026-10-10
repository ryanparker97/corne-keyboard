# macOS data engineering / DevOps keymap

This 42-key Corne layout targets data engineering and DevOps work on macOS: SQL, Python, shell, YAML/JSON, Terraform/HCL, Docker, Kubernetes, Vim, and tmux. It intentionally uses **no home-row mods, sticky modifiers, tap dance, or combos**. Letters are ordinary keys. Two hold-taps exist and both sit on outer keys: `TAB/HYP` (left outer home key, the same on every layer) and `RET/WM` (right outer thumb).

There is no objectively best keymap. This one favors familiar QWERTY positions, mnemonic navigation, short finger travel, and a small number of focused layers.

## Base thumb keys

```text
left hand                 right hand
OPTION RAISE  COMMAND   |  SPACE  LOWER  ENTER/WM
```

- Hold **RAISE** for data, infrastructure, and shell symbols.
- Hold **LOWER** for numbers, navigation, terminal prefixes, and function keys.
- Hold **RAISE + LOWER** for system controls.
- Hold **ENTER/WM** (tap sends Enter) for window-manager chords.

## Base — `Base`

```text
ESC   Q     W     E     R     T   |  Y     U     I     O     P     BSPC
TAB/HYP A   S     D     F     G   |  H     J     K     L     ;     '
SHIFT Z     X     C     V     B   |  N     M     ,     .     /     CTRL
                OPT   RAISE  CMD  |  SPACE  LOWER  ENTER/WM
```

Option and Command are on Base-layer thumbs for macOS shortcuts. **Esc** is the top-left key. The left outer home key is **Tab when tapped and Hyper when held**; Hyper is Ctrl+Alt+Cmd+Shift (skhd's built-in `hyper`), and the same key sits in the same place on every layer. Right Control is the bottom-right key, so `Ctrl-h/j/k/l` is a right-pinky chord with the left hand free for the letter. The left outer thumb becomes Control on the other layers, keeping layered navigation and terminal chords accessible. Alpha keys never change meaning based on tap duration.

`TAB/HYP` uses the `balanced` flavor with a 200 ms tapping term and `require-prior-idle-ms = 100`: Tab resolves instantly while typing, and a hold becomes Hyper when the next key is tapped or the term expires. Nothing is bound to Hyper in this repo yet; the WM layer still sends `Ctrl+Alt`, so skhd is unchanged.

## Lower — `Nav/Num`

```text
ESC   1     2     3     4     5   |  6     7     8     9     0     BSPC
TAB/HYP CTRL OPT  CMD   SHIFT TMUX|  LEFT  DOWN  UP    RIGHT PGDN  PGUP
F1    F2    F3    F4    F5    F6  |  F7    F8    F9    F10   F11   F12
                CTRL  RAISE  CMD  |  SPACE  LOWER  ENTER
```

The navigation row deliberately puts arrows on physical **H/J/K/L**. The left-hand modifiers are ordinary held keys, so macOS editing stays ergonomic and predictable:

- `LOWER + Option + Left/Right`: move by word.
- `LOWER + Command + Left/Right`: move to the start/end of a line.
- `LOWER + Command + Up/Down`: move to the start/end of a document.
- Add `LOWER + Shift` to extend the selection.

`TMUX` emits and releases the `Ctrl-A` prefix (matching `tmux/tmux.conf` in the dotfiles repo); tap a Lower-layer arrow next to move between tmux panes. Releasing Control inside the prefix macro avoids accidentally sending `Ctrl-Arrow` as the follow-up command. The old `VIM` (`Ctrl-W`) macro was removed to free the left home outer key for `TAB/HYP`; use Right Control + `W` for Vim window commands.

## Raise — `Symbols`

```text
ESC   !     @     #     $     %   |  ^     &     *     :     |     BSPC
TAB/HYP CTRL OPT  CMD   SHIFT =   |  [     (     )     {     }     ]
\     -     "     _     +     `   |  <     >     HOME  END   ?     ~
                CTRL  RAISE  CMD  |  SPACE  LOWER  ENTER
```

The left half mirrors the normal shifted number order, reducing memorization. The right home row groups the brackets as `[ ( ) { } ]`, with the parentheses on the index and middle fingers because they are the most frequent; `:` and `|` sit directly above. Python's underscore, colon, double quote, parentheses, decorators (`@`), comments (`#`), f-string braces, arithmetic operators, comparisons are all direct. Backtick, `-`, `=`, `$`, `?`, pipe, and backslash remain direct for SQL, shell, and infrastructure code. Comma, period, slash, semicolon and the single quote stay in their Base positions. `BSPC`, `TAB` (the `TAB/HYP` key), `HOME` and `END` are available without leaving the layer, so `foo(<BS>` does not need a layer release. `~` sits at the bottom-right where `DEL` used to be; forward-delete is no longer on Raise.

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
ESC   BT1   BT2   BT3   BT4   BT5 |  CAP   CWORD CAPS  SPOT  APP   LOCK
TAB/HYP PREV PLAY  NEXT  MUTE  VOL- |  MC    EXPO  DT<   DT>   AREA  FQUIT
RESET DISP- DISP+ USB   BLE   VOL+ |  BTCLR FULL  WIN   HIDE  MIN   BOOT
                CTRL  RAISE  CMD  |  SPACE  LOWER  ENTER
```

- `CAP`: macOS **Shift-Command-5** capture UI for screenshots and recordings.
- `CWORD`: Caps Word, convenient for SQL keywords such as `SELECT` and constants such as `MAX_RETRIES`; it stops automatically on normal word-breaking input. The old both-Shift combo was removed because the bottom-right key is now Right Control.
- `CAPS`: traditional Caps Lock remains available.
- `SPOT`, `APP`, `LOCK`: Spotlight, app switcher, and screen lock.
- `MC`, `EXPO`, `DT<`, `DT>`: Mission Control, App Exposé, and desktop left/right (Ctrl-arrows).
- `AREA`, `FULL`: Shift-Command-4 and Shift-Command-3 screenshots. `FQUIT`: Force Quit. `WIN`: next window of the app. `HIDE`, `MIN`: hide and minimize.
- Bluetooth, USB/BLE output, media, brightness, bootloader, and reset controls are retained. `BOOT` (bootloader) moved to the bottom-right and `BTCLR` (Bluetooth clear) replaced `OUT` (output toggle, redundant with `USB` and `BLE`). The RGB underglow keys that used to live on the right two rows were dead while `CONFIG_ZMK_RGB_UNDERGLOW=n`; restore them from git history if you re-enable RGB.

## WM — `Window manager`

```text
TAB   .     .     E     R     T   |  1     2     3     4     5     .
.     A     S     D     F     .   |  H     J     K     L     .     .
.     Z     X     .     V     B   |  .     M     .     .     .     .
                .     .     .     |  TERM  .     (held)
```

Hold the right outer thumb. Every key sends `Ctrl+Alt+<key>` at its normal QWERTY position, so the layer drives the dotfiles' `skhd/skhdrc` without any chord gymnastics: `H/J/K/L` focus, `1-5` focus Spaces, `M`/`S`/`E` enter move/swap/resize modes, and `Z F B R X V A D T TAB` are zoom, fullscreen, balance, rotate, split, mirror, stack, bsp, float, and focus-recent. `TERM` (the Space key) opens a new Alacritty window. In move/swap/resize mode, release the layer and tap the plain `H/J/K/L` or `1-5` key.

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
