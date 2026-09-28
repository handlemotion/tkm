# TheKeyMachine - Animation toolset for Maya animators

<img width="269px" src="./TheKeyMachine/data/img/tkm_logo_small.png" alt="TheKeyMachine logo" />

TheKeyMachine (TKM) is an open source animation toolset for Autodesk Maya, originally developed by Rodrigo Torres.

This repository is an independently maintained continuation of the original GPL-3.0 project. It is not endorsed or certified by Autodesk, and independent maintenance does not imply endorsement by the upstream project.

## Current release

**Beta 0.1.6 / Build 308 - 28 September 2026**

This patch fixes selection-set creation and display, makes upgrades replace the existing installation while preserving its configuration, and persists one toolbar shelf button across Maya restarts.

Maya 2027 on Windows 11 and macOS Tahoe 26.6.2 or newer is the current development target. This is not a claim of complete compatibility or Autodesk certification. Full installation and tool testing on those platforms is still required for a verified support claim. Use Maya's bundled Python, PySide, and shiboken packages; do not install replacement Qt bindings into Maya.

## Installation

1. Download and extract the release ZIP. Keep the versioned installer beside the `TheKeyMachine` folder. Source checkouts use `TheKeyMachine_Drag&Drop_installer.py`.
2. If upgrading, leave the existing installation in place. The installer replaces the single `TheKeyMachine` code folder and preserves its configuration and separate `TheKeyMachine_user_data` folder.
3. Start the Maya version you want to install into.
4. Drag the versioned installer, such as `TheKeyMachine_Installer_v0_1_6.py`, into the Maya viewport.
5. Accept the GPL-3.0 license and click **Install TheKeyMachine**.
6. Restart Maya so its updated `Maya.env` is loaded.

Each patch ships a uniquely named installer so Maya cannot reuse an older drag-and-drop module from memory. The installer replaces the code in Maya's user scripts directory, restores the previous copy if installation fails, updates one shelf button, and adds a marked `XBMLANGPATH` block to that Maya version's `Maya.env`. Re-running the installer does not stack code folders, shelf buttons, or environment blocks. Unrelated `Maya.env` content is preserved. Installation does not require the retired upstream website or registration service.

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
