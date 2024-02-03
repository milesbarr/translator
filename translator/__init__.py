import logging
import os
from pathlib import Path
from typing import MutableMapping

from ._html_translator import translate_html
from ._rss_feed_translator import translate_rss_feed
from ._text_translator import translate_text
from ._utils import is_translatable_text, normalize_language_tag, split_language_tag
from ._web_app_manifest_translator import translate_web_app_manifest


__all__ = [
    "translate_html",
    "translate_rss_feed",
    "translate_text",
    "is_translatable_text",
    "normalize_language_tag",
    "split_language_tag",
    "translate_web_app_manifest",
    "translate_file",
    "translate_directory",
]


_logger = logging.getLogger(__name__)

_TRANSLATE_BY_EXT = {
    ".html": translate_html,
    ".rss": translate_rss_feed,
    ".webmanifest": translate_web_app_manifest,
}


def translate_file(
    input_file_path: str | bytes | os.PathLike,
    output_file_path: str | bytes | os.PathLike,
    source_language: str,
    target_language: str,
    cache: MutableMapping[str, str],
) -> None:
    """
    Translates the content of a file from one language to another.

    Args:
        input_file_path (str | bytes | os.PathLike): Path to the input file.
        output_file_path (str | bytes | os.PathLike]): Path to the output file where the translated text will be saved.
        source_language (str): The IETF language tag for the source language.
        target_language (str): The IETF language tag for the target language.
        cache (MutableMapping[str, str]): A cache to store and retrieve pre-translated phrases for efficiency.

    Note:
        The function determines the translation approach based on the file extension.
    """
    input_file_path = Path(input_file_path)
    output_file_path = Path(output_file_path)
    ext = {"manifest.json": ".webmanifest", "feed.xml": ".rss"}.get(
        input_file_path.name, input_file_path.suffix
    )
    translate = _TRANSLATE_BY_EXT.get(ext)
    if not translate:
        return
    _logger.info("Translating file %s to %s", input_file_path, output_file_path)
    with input_file_path.open() as f:
        content = f.read()
    translated_content = translate(content, source_language, target_language, cache)
    with output_file_path.open("w") as f:
        f.write(translated_content)


def translate_directory(
    input_dir: str | bytes | os.PathLike,
    output_dir: str | bytes | os.PathLike,
    source_language: str,
    target_language: str,
    cache: MutableMapping[str, str],
    exclude_paths: list[str | bytes | os.PathLike] = [],
) -> None:
    """
    Translate all files within a specified directory from one language to another.

    This function recursively traverses the input directory, translating the content of each file from the source
    language to the target language. The translated files are saved in the output directory, preserving the
    original directory structure. Files in `exclude_paths` are skipped during translation.

    Args:
        input_dir (str | bytes | os.PathLike): The path to the input directory containing files to be translated.
        output_dir (str | bytes | os.PathLike): The path to the output directory where the translated files will be saved.
        source_language (str): The IETF language tag for the source language.
        target_language (str): The IETF language tag for the target language.
        cache (MutableMapping[str, str]): A cache to store and retrieve pre-translated phrases for efficiency.
        exclude_paths (list[str | bytes | os.PathLike], optional): A list of paths to exclude from translation. Defaults to an empty list.

    Example:
        translate_directory(
            input_dir="/path/to/input",
            output_dir="/path/to/output",
            source_language="en",
            target_language="es",
            cache={},
            exclude_paths=["/path/to/input/skip"]
        )

    Note:
        - Ensure that the source and target languages are specified in valid IETF format.
        - The paths in `exclude_paths` should be absolute or relative to the input directory.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    exclude_paths = [Path(path) for path in exclude_paths]

    for root, _, files in os.walk(input_dir):
        for input_file_name in files:
            input_file_path = Path(root) / input_file_name
            if any(
                input_file_path.is_relative_to(exclude_path)
                for exclude_path in exclude_paths
            ):
                continue
            output_file_path = output_dir / input_file_path.relative_to(root)
            translate_file(
                input_file_path,
                output_file_path,
                source_language,
                target_language,
                cache,
            )
