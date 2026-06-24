import pytest
import cssutils
import logging

# Suppress cssutils warnings for standard CSS
cssutils.log.setLevel(logging.CRITICAL)

@pytest.fixture
def stylesheet():
    """Parses the CSS file for testing."""
    with open("style.css", "r") as f:
        return cssutils.parseString(f.read())

def test_add_button_color_is_not_black(stylesheet):
    """
    Verifies the #add-btn specifically uses the accent color, 
    not black (reproducing the distinction between button types).
    """
    rule = next(r for r in stylesheet if r.selectorText == "#add-btn")
    assert rule.style.backgroundColor == "var(--accent)"
    assert rule.style.color == "#ffffff"

def test_todo_actions_button_color_is_black(stylesheet):
    """
    Verifies the fix: .todo-actions button must have black text color.
    This test would have failed if the color was set to a different value.
    """
    rule = next(r for r in stylesheet if r.selectorText == ".todo-actions button")
    # Normalize color to hex for comparison
    color = cssutils.css.CSSValue(rule.style.color).cssText
    assert color == "#000000"

def test_button_background_is_transparent(stylesheet):
    """
    Edge case: Ensure that while the text is black, the background 
    remains transparent for todo-actions buttons.
    """
    rule = next(r for r in stylesheet if r.selectorText == ".todo-actions button")
    assert rule.style.backgroundColor == "transparent"
