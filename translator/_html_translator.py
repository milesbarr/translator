from ._text_translator import translate_text
from ._utils import normalize_language_tag
from bs4 import BeautifulSoup, Comment, Declaration, Doctype, NavigableString, Tag
from typing import MutableMapping

_TRANSLATABLE_META_NAMES = [
    "description",
    "twitter:title",
    "twitter:description",
    "twitter:image:alt",
]

_TRANSLATABLE_META_PROPERTIES = [
    "og:title",
    "og:description",
    "og:image:alt",
]

_TRANSLATABLE_HTML_ATTRIBUTES = [
    "title",
    "aria-label",
    "aria-placeholder",
    "aria-describedby",
    "placeholder",
    "value",
    "label",
    "alt",
]


def _is_element_translatable(element: Tag | None) -> bool:
    """
    Determine if a BeautifulSoup element is translatable according to HTML `translate` attribute rules.

    This function checks if the provided BeautifulSoup element should be considered translatable
    based on the `translate` attribute. The `translate` attribute can be set to "yes" or "no".
    By default, elements are translatable if the `translate` attribute is not explicitly set.
    The function respects the hierarchical structure of HTML, meaning if an ancestor of an element
    has `translate="no"`, the element is not translatable unless it has its own `translate="yes"`.

    Additionally, the function excludes elements within '<script>' and '<style>' tags from being
    considered translatable, as their content is typically not meant for translation.

    Args:
        element (Tag | None): The BeautifulSoup element to check. This should be an instance of
                              BeautifulSoup's Tag class. If None is provided, the function returns
                              False, assuming non-translatable content.

    Returns:
        bool: True if the element is considered translatable, False otherwise.
    """
    while element is not None:
        if element.name in {"script", "style"}:
            return False
        if "translate" in element.attrs:
            return element.attrs["translate"] == "yes"
        element = element.parent
    return True


def _translate_meta_tag_content(
    soup: BeautifulSoup,
    source_language: str,
    target_language: str,
    cache: MutableMapping[str, str],
):
    """
    Translate meta tag content within the BeautifulSoup object.

    Args:
        soup (BeautifulSoup): BeautifulSoup object representing the HTML document.
        source_language (str): The IETF language tag for the source language.
        target_language (str): The IETF language tag for the target language.
        cache (MutableMapping[str, str]): A cache to store and retrieve pre-translated phrases for efficiency.
    """
    for meta_tag in soup.find_all("meta", content=True):
        if (
            meta_tag.get("name") in _TRANSLATABLE_META_NAMES
            or meta_tag.get("property") in _TRANSLATABLE_META_PROPERTIES
        ):
            if _is_element_translatable(meta_tag):
                meta_tag["content"] = translate_text(
                    meta_tag["content"], source_language, target_language, cache
                )


def translate_html(
    html: str,
    source_language: str,
    target_language: str,
    cache: MutableMapping[str, str],
) -> str:
    """
    Translate the text within HTML content to a specified language.

    This function updates the `lang` attribute of the HTML tag, modifies `og:locale` meta tag,
    translates various meta tags and textual content, and updates specific attributes like
    `title`, `aria-label`, and `alt` based on a provided translation function.

    Args:
        html (str): The HTML content to be translated.
        source_language (str): The IETF language tag for the source language.
        target_language (str): The IETF language tag for the target language.
        cache (MutableMapping[str, str]): A cache to store and retrieve pre-translated phrases for efficiency.

    Returns:
        str: The translated HTML content.
    """
    # Parse the HTML.
    soup = BeautifulSoup(html, "html.parser")

    # Normalize the target language.
    target_language = normalize_language_tag(target_language)

    # Update the `lang` attribute of the `<html>` tag.
    html_tag = soup.find("html")
    if html_tag:
        html_tag["lang"] = target_language

    # Update the the `og:locale` meta tag.
    og_locale_meta = soup.find("meta", property="og:locale")
    if og_locale_meta:
        og_locale_meta["content"] = target_language.replace("-", "_", 1)

    # Translate meta tags.
    _translate_meta_tag_content(soup, source_language, target_language, cache)

    # Translate text elements.
    for text_node in soup.find_all(string=True):
        if (
            isinstance(text_node, NavigableString)
            and not isinstance(text_node, (Comment, Doctype, Declaration))
            and isinstance(text_node.parent, Tag)
            and text_node.strip()
            and _is_element_translatable(text_node.parent)
        ):
            text_node.replace_with(
                translate_text(text_node, source_language, target_language, cache)
            )

    # Translate attributes.
    for attr in _TRANSLATABLE_HTML_ATTRIBUTES:
        for element in soup.find_all(attrs={attr: True}):
            if _is_element_translatable(element):
                element[attr] = translate_text(
                    element[attr], source_language, target_language, cache
                )

    # Return the translated HTML.
    return str(soup)
