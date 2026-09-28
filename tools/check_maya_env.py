#!/usr/bin/env python3
"""Check Maya.env marker removal in the installer and uninstaller."""

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    "TheKeyMachine_Drag&Drop_installer.py",
    "TheKeyMachine/mods/uiMod.py",
)


def load_remove_function(path: str):
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
        elif isinstance(node, ast.FunctionDef) and node.name == "_remove_tkm_env_blocks":
            nodes.append(node)

    namespace = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), path, "exec"), namespace)
    return namespace["_remove_tkm_env_blocks"]


def main():
    for path in SOURCES:
        remove_blocks = load_remove_function(path)
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
    print("Maya.env markers removed once; BOM and unrelated lines preserved")


if __name__ == "__main__":
    main()
