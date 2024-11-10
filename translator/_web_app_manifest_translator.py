import json
from typing import MutableMapping

from ._text_translator import translate_text


def translate_web_app_manifest(
    manifest: str,
    source_language: str,
    target_language: str,
    cache: MutableMapping[str, str],
) -> str:
    data = json.loads(manifest)
    if "description" in manifest:
        data["description"] = translate_text(
            data["description"], source_language, target_language, cache
        )
    for shortcut in data.get("shortcuts", []):
        if "name" in shortcut:
            shortcut["name"] = translate_text(shortcut["name"])
        if "short_name" in shortcut:
            shortcut["short_name"] = translate_text(
                shortcut["short_name"], source_language, target_language, cache
            )
    return json.dumps(data)
