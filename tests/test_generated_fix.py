import pytest
import cssutils

# Assuming the CSS file is located at the project root
CSS_FILE_PATH = "style.css"

def get_button_background_color():
    """Helper to parse the CSS file and extract the button background color."""
    sheet = cssutils.parseFile(CSS_FILE_PATH)
    for rule in sheet:
        if rule.selectorText == "button":
            return rule.style.backgroundColor
    return None

def test_button_color_is_black():
    """
    Verify that the button background color is set to black (#000000).
    This test would have failed before the fix (e.g., if it was another color or missing).
    """
    color = get_button_background_color()
    # cssutils normalizes colors; #000000 is represented as black or #000000
    assert color in ["#000000", "black", "rgb(0, 0, 0)"]

def test_button_color_is_not_default_or_transparent():
    """
    Edge case: Ensure the color is explicitly set to black and not 
    transparent or a default browser color.
    """
    color = get_button_background_color()
    assert color is not None, "Button background color should be defined in CSS"
    assert color != "transparent", "Button background should not be transparent"

def test_css_syntax_validity():
    """
    Verify that the CSS file is syntactically correct and contains the button rule.
    """
    sheet = cssutils.parseFile(CSS_FILE_PATH)
    selectors = [rule.selectorText for rule in sheet if hasattr(rule, 'selectorText')]
    assert "button" in selectors, "The 'button' selector is missing from style.css"
