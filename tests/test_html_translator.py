import unittest
from translator._html_translator import translate_html


class TestHTMLTranslator(unittest.TestCase):
    def test_update_html_lang_attribute(self):
        original_html = '<html lang="en-US"></html>'
        expected_html = '<html lang="es-ES"></html>'
        self.assertEqual(
            translate_html(original_html, "en-US", "es-ES", {}), expected_html
        )

    def test_update_og_locale_meta_tag(self):
        original_html = '<meta content="en_US" property="og:locale"/>'
        expected_html = '<meta content="es_ES" property="og:locale"/>'
        self.assertEqual(
            translate_html(original_html, "en-US", "es-ES", {}), expected_html
        )

    def test_translate_meta_tag_content(self):
        original_html = '<meta content="Hello, World!" name="description"/>'
        expected_html = '<meta content="¡Hola Mundo!" name="description"/>'
        cache = {"Hello, World!": "¡Hola Mundo!"}
        self.assertEqual(translate_html(original_html, "en-US", "es-ES", cache), expected_html)

    def test_translate_text_nodes(self):
        original_html = "<p>Hello, World!</p>"
        expected_html = "<p>¡Hola Mundo!</p>"
        cache = {"Hello, World!": "¡Hola Mundo!"}
        self.assertEqual(translate_html(original_html, "en-US", "es-ES", cache), expected_html)

    def test_translate_text_nodes_with_translate_attribute_no(self):
        original_html = '<p translate="no">Hello, World!</p>'
        expected_html = '<p translate="no">Hello, World!</p>'
        cache = {"Hello, World!": "¡Hola Mundo!"}
        self.assertEqual(translate_html(original_html, "en-US", "es-ES", cache), expected_html)

    def test_translate_text_nodes_with_translate_attribute_yes(self):
        original_html = (
            '<p translate="no">Hello, <span translate="yes">World</span>!</p>'
        )
        expected_html = (
            '<p translate="no">Hello, <span translate="yes">Mundo</span>!</p>'
        )
        cache = {"World": "Mundo"}
        self.assertEqual(translate_html(original_html, "en-US", "es-ES", cache), expected_html)

    def test_translate_element_attributes(self):
        original_html = '<img alt="Hello, World!"/>'
        expected_html = '<img alt="¡Hola Mundo!"/>'
        cache = {"Hello, World!": "¡Hola Mundo!"}
        self.assertEqual(translate_html(original_html, "en-US", "es-ES", cache), expected_html)


if __name__ == "__main__":
    unittest.main()
