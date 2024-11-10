from collections.abc import MutableMapping
from deep_translator import GoogleTranslator
import time
import re
from typing import MutableMapping

from ._utils import is_translatable_text, normalize_language_tag, split_language_tag


def translate_text(
    text: str,
    source_language_tag: str,
    target_language_tag: str,
    cache: MutableMapping[str, str],
) -> str:
    """
    Translate text with caching using a provided translation function.

    Args:
        text (str): The text to be translated.
        source_language_tag (str): The IETF language tag for the source language.
        target_language_tag (str): The IETF language tag for the target language.
        cache (MutableMapping[str, str]): A cache to store and retrieve pre-translated phrases for efficiency.

    Returns:
        str: The translated text.
    """
    if not is_translatable_text(text):
        return text

    source_language_tag = normalize_language_tag(source_language_tag)
    target_language_tag = normalize_language_tag(target_language_tag)
    if source_language_tag == target_language_tag:
        return text

    # Extract leading and trailing whitespace using regex.
    leading_whitespace = re.match(r"\s*", text).group()
    trailing_whitespace = re.search(r"\s*$", text).group()
    stripped_text = text.strip()

    # Check if the translation is already cached.
    if translated_text := cache.get(stripped_text):
        return leading_whitespace + translated_text + trailing_whitespace

    # Translate the text using Google Translate.
    time.sleep(1)
    source_language_code, _ = split_language_tag(source_language_tag)
    target_language_code, _ = split_language_tag(target_language_tag)
    translated_text = GoogleTranslator(
        source=source_language_code, target=target_language_code
    ).translate(text)

    # Store the translated text in the cache.
    cache[stripped_text] = translated_text

    return leading_whitespace + translated_text + trailing_whitespace
