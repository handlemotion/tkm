# TheKeyMachine - Animation toolset for Maya animators

<img width="269px" src="./TheKeyMachine/data/img/tkm_logo_small.png" alt="TheKeyMachine logo" />

TheKeyMachine (TKM) is an open source animation toolset for Autodesk Maya, originally developed by Rodrigo Torres.

This repository is an independently maintained continuation of the original GPL-3.0 project. It is not endorsed or certified by Autodesk, and independent maintenance does not imply endorsement by the upstream project.

## Current release

**Beta 0.1.5 / Build 307 - 28 September 2026**

This release adds installer support for the Python 3.13 runtime used by Maya 2027, keeps the existing Maya 2022-2025 and Linux fallbacks, and prevents duplicate TheKeyMachine blocks in `Maya.env`.

Maya 2027 on Windows 11 and macOS Tahoe 26.6.2 or newer is the current development target. This is not a claim of complete compatibility or Autodesk certification. Full installation and tool testing on those platforms is still required for a verified support claim. Use Maya's bundled Python, PySide, and shiboken packages; do not install replacement Qt bindings into Maya.

## Installation

1. Download or clone the complete repository and keep `TheKeyMachine_Drag&Drop_installer.py` beside the `TheKeyMachine` folder.
2. If upgrading, back up `TheKeyMachine_user_data`, then uninstall the existing code or remove only the old `TheKeyMachine` code folder from Maya's scripts directory. Keep `TheKeyMachine_user_data` so custom scripts, preferences, selection sets, and saved animation data remain available.
3. Start the Maya version you want to install into.
4. Drag `TheKeyMachine_Drag&Drop_installer.py` into the Maya viewport.
5. Accept the GPL-3.0 license and click **Install TheKeyMachine**.
6. Restart Maya so its updated `Maya.env` is loaded.

The installer copies the code into Maya's user scripts directory and adds a marked `XBMLANGPATH` block to that Maya version's `Maya.env`. Re-running the environment update does not add the block again, and unrelated `Maya.env` content is preserved. Installation does not require the retired upstream website or registration service.

For a studio installation, configure `INSTALL_PATH` and `USER_FOLDER_PATH` in `TheKeyMachine/data/config/config.json`. Keep the installed code separate from `TheKeyMachine_user_data` and make both locations available on Maya's Python path where required.

## Features

- Animation tools including Isolate, Snap, Reset, Counter, Temp Pivot, FollowCam, Anim Offset, Copy and Paste Animation, Copy and Paste World Position, and an advanced curve editor
- Selection Manager for selection sets
- Tween and Blend sliders
- Customizable tool and script menus

<img src="./TheKeyMachine/data/img/toolbar_example.png" alt="TheKeyMachine toolbar" />

<img width="200px" src="./TheKeyMachine/data/img/install_example.png" alt="TheKeyMachine installer" />

## License and upstream status

TheKeyMachine remains licensed under the [GNU General Public License v3.0](./license_gpl-3.0.txt). Preserve the original author attribution and GPL terms when modifying or redistributing it.

The original project announced the end of active upstream development and the shutdown of its website. This fork is maintained independently and does not depend on that website for installation or normal operation.
