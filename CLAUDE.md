# CLAUDE.md

QMK userspace for one keyboard: Glorious GMMK V2 96% ISO, keymap `acooke`.

- Keymap: `keyboards/gmmk/gmmk2/p96/iso/keymaps/acooke/keymap.c`
- Diagram shown in README: `keyboards/gmmk/gmmk2/p96/iso/keymaps/acooke/keymap.svg` (generated, never edit by hand)
- Diagram generator: `tools/keymap_svg.py`
- Firmware is built by GitHub Actions on every push and published to the `latest` release.
- A pre-commit hook (`.githooks/pre-commit`) regenerates `keymap.svg` whenever `keymap.c` is committed. In a fresh clone, enable it once with `git config core.hooksPath .githooks`. Check it is enabled with `git config core.hooksPath` (should print `.githooks`).

## Rule: keymap changes must update the docs in the same commit

Whenever `keymap.c` changes, follow every step below before committing. Do not skip steps.

### Step 1: Make the keymap change

Edit `keymap.c`. Keep these constraints:

- Each `LAYOUT(...)` must contain exactly 100 keycodes.
- Layer order is fixed: first `LAYOUT` is the base layer, second is the Fn layer (`_FL`).
- Do not raise `DYNAMIC_KEYMAP_LAYER_COUNT` in `config.h` above 3. More layers do not fit in the keyboard's settings storage and the build fails with "Dynamic keymaps are configured to use more EEPROM than is available".
- If you add a new custom keycode to `enum custom_keycodes`, also handle it in `process_record_user` and give it a colour in `overlay_color` (both in `keymap.c`).
- Keep the file's existing line endings (CRLF).

### Step 2: Regenerate the diagram

The pre-commit hook does this automatically, but run it yourself first so any error shows up before you commit. From the repo root run:

```
python tools/keymap_svg.py
```

Expected output: `wrote keyboards/.../keymap.svg`.

If it prints `error: add these keycodes to BASE_LABELS or FN_LABELS`:

1. Open `tools/keymap_svg.py`.
2. For each keycode listed:
   - If it is on the base layer, add it to `BASE_LABELS` as `"KC_NAME": "Legend"`.
   - If it is on the Fn layer, add it to `FN_LABELS` as `"KC_NAME": ("Label", "category")`.
   - Labels must be 8 characters or fewer so they fit on a key.
   - `category` must be one of: `light` (lighting controls), `media` (media and app keys), `toggle` (on/off features), `boot` (bootloader), `red`, `white`, `rainbow` (lighting presets).
3. Run `python tools/keymap_svg.py` again. Repeat until it prints `wrote ...`.

Any other `error:` means `keymap.c` is malformed (wrong key count or missing layer). Fix `keymap.c`, then run the script again.

### Step 3: Update README.md by hand

Open `README.md` and make the text match the new keymap:

1. **Fn shortcuts** tables (Lighting / Media and apps / System): add, remove or change rows for every Fn-layer key that changed. Format: `| Fn + Key | What it does |`.
2. **What the lights mean while Fn is held** table: update only if colours or overlay behaviour in `keymap.c` changed.
3. **Notes** list: update if layer count, preset keycodes or bootloader keys changed.

Do not touch the "About this repo (QMK Userspace)" section.

### Step 4: Check before committing

Run:

```
git status --short
git diff --stat
```

Confirm:

- `keymap.c`, `keymap.svg` and `README.md` all appear as modified (plus `tools/keymap_svg.py` if you added labels).
- No other files changed unexpectedly.

### Step 5: Commit and push

```
git add -A
git commit -m "<what changed in the keymap>"
git push
```

### Step 6: Confirm the firmware built

```
gh run list -L 1
gh run watch <run id from the previous command> --exit-status
```

If the run fails, open the log with `gh run view <run id> --log-failed`, fix the error in `keymap.c`, and repeat from Step 2.

Report to the user: what changed, that the diagram and README were updated, and whether the build passed.
