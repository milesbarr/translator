def is_translatable_text(text: str, min_length: int = 2) -> bool:
    """
    Check if the provided text is translatable. This means the text should be non-empty,
    not entirely numeric, not just whitespace, and meet a minimum length requirement.

    Args:
        text (str): The text to be checked.
        min_length (int): Minimum length of text to be considered translatable.

    Returns:
        bool: True if the text is translatable, False otherwise.
    """
    text = text.strip()
    return text and len(text) >= min_length and not text.isdigit()


def split_language_tag(language_tag: str) -> tuple[str, str | None]:
    """
    Split an IETF language tag into its language code and optional country/region code.

    This function takes a language tag (like 'en-US' or 'fr_CA') and splits it
    into two parts: the language code (e.g., 'en', 'fr') and an optional
    country/region code (e.g., 'US', 'CA'). If the country/region code is not
    present in the input, None is returned in its place.

    The function also normalizes the input by replacing underscores ('_') with
    hyphens ('-') to ensure consistent formatting according to IETF BCP 47 standard.

    Args:
        language_tag (str): The IETF language tag to split, formatted as 'language-region'
                            or 'language_region'.

    Returns:
        tuple[str, str | None]: A tuple containing the language code and an optional
                                country/region code. The country/region code is None if
                                it's not present in the input.

    Examples:
        >>> split_language_tag("en-US")
        ('en', 'US')
        >>> split_language_tag("fr_CA")
        ('fr', 'CA')
        >>> split_language_tag("de")
        ('de', None)
    """
    language_tag = language_tag.replace("_", "-")
    parts = language_tag.split("-", 1)
    language_code = parts[0]
    region_code = parts[1] if len(parts) > 1 else None
    return language_code, region_code


def normalize_language_tag(language_tag: str) -> str:
    """
    Normalize an IETF language tag for consistent formatting.

    This function converts the language code to lowercase and the country/region code
    (if present) to uppercase. The standardized format for IETF language tags is used,
    where language code and country/region code are separated by a hyphen.

    Args:
        language_tag (str): The IETF language tag to be normalized. Expected in formats like
                            "en", "en-US", "EN-us", "en_us", or "EN_US".

    Returns:
        str: The normalized language tag, with the language code in lowercase and the
             country/region code in uppercase, separated by a hyphen.

    Examples:
        >>> normalize_language_tag("en-US")
        'en-US'
        >>> normalize_language_tag("fr_ca")
        'fr-CA'
        >>> normalize_language_tag("DE")
        'de'
    """
    language_code, region_code = split_language_tag(language_tag)
    normalized_language_tag = language_code.lower()
    if region_code:
        normalized_language_tag += "-" + region_code.upper()
    return normalized_language_tag
