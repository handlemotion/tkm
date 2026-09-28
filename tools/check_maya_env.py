#!/usr/bin/env python3
"""Check Maya.env marker removal in the installer and uninstaller."""

import ast
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    "TheKeyMachine_Drag&Drop_installer.py",
    "TheKeyMachine/mods/uiMod.py",
)


def load_functions(path: str):
    source = ROOT / path
    tree = ast.parse(source.read_bytes(), filename=path)
    names = {"TKM_ENV_START", "TKM_ENV_END"}
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id in names
            for target in node.targets
        ):
            nodes.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in {"_remove_tkm_env_blocks", "_update_tkm_env_data"}:
            nodes.append(node)

    namespace = {"re": re}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), path, "exec"), namespace)
    return namespace


def main():
    for path in SOURCES:
        remove_blocks = load_functions(path)["_remove_tkm_env_blocks"]
        start = b"# THIS LINE IS HERE FOR UNINSTALLING PURPOSES, PLEASE DO NOT TOUCH. START OF THEKEYMACHINE CODE"
        end = b"# END OF THEKEYMACHINE CODE"
        bom = b"\xef\xbb\xbf"
        source = (
            bom
            + b"CUSTOM_BEFORE = keep\r\n"
            + start + b"\r\nXBMLANGPATH = old\r\n" + end + b"\r\n"
            + b"CUSTOM_AFTER = keep\r\n"
            + start + b"\nXBMLANGPATH = duplicate\n" + end + b"\n"
        )
        expected = bom + b"CUSTOM_BEFORE = keep\r\nCUSTOM_AFTER = keep\r\n"
        assert remove_blocks(source) == expected, path
        assert remove_blocks(expected) == expected, path

    update_env = load_functions(SOURCES[0])["_update_tkm_env_data"]
    original = bom + b"CUSTOM_ICON_ROOT = C:/custom icons\r\nXBMLANGPATH = %CUSTOM_ICON_ROOT%\r\nOTHER=keep"
    updated = update_env(original, "C:/maya/TheKeyMachine/data/img", True)
    assert updated.index(b"CUSTOM_ICON_ROOT") < updated.index(start) < updated.index(b"XBMLANGPATH = %CUSTOM_ICON_ROOT%")
    assert b"XBMLANGPATH = C:/maya/TheKeyMachine/data/img;%CUSTOM_ICON_ROOT%\r\n" in updated
    assert remove_blocks(updated) == original
    assert update_env(updated, "C:/maya/TheKeyMachine/data/img", True).count(start) == 1

    incomplete = b"CUSTOM=keep\n" + start + b"\nXBMLANGPATH = /old:$CUSTOM"
    assert remove_blocks(update_env(incomplete, "/new", False)) == incomplete
    print("Maya.env update preserves bytes and combines the first effective XBMLANGPATH")


if __name__ == "__main__":
    main()
