import xml.etree.ElementTree as ET
from typing import MutableMapping

from ._text_translator import translate_text
from ._utils import normalize_language_tag


def translate_rss_feed(
    xml: str,
    source_language: str,
    target_language: str,
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
    # Parse the XML.
    root = ET.fromstring(xml)

    # Update the `<language>` element.
    language_element = root.find("./channel/language")
    if language_element is not None:
        language_element.text = normalize_language_tag(target_language).lower()

    # Translate `<item>` elements.
    for item in root.findall("./channel/item"):
        title_element = item.find("title")
        if title_element is not None and title_element.text:
            title_element.text = translate_text(
                title_element.text, source_language, target_language, cache
            )

        description_element = item.find("description")
        if description_element is not None and description_element.text:
            description_element.text = translate_text(
                description_element.text, source_language, target_language, cache
            )

    return ET.tostring(root)
