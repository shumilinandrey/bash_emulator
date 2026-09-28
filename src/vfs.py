import json
import base64
from typing import Any


def load_vfs(path: str) -> dict[str, Any] | None:
    with open(path, "r", encoding="utf-8") as file:
        vfs = json.load(file)
        if not isinstance(vfs, dict):
            return None
    return vfs


def get_node(vfs: dict[str, Any], path: str) -> dict[str, Any] | None:
    if path in ("", "/"):
        return vfs

    parts = [i for i in path.split("/") if i]
    node = vfs
    for part in parts:
        if node.get("type") != "directory":
            return None
        children = node.get("children", {})
        if part not in children:
            return None
        node = children[part]
    return node


def read_file(node: dict[str, Any]) -> str | None:
    if node.get("type") != "file":
        return None
    return node.get("content", "Файл пустой")


