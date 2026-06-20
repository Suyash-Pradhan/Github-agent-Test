import pytest
from tinycss2.parser import parse_stylesheet
from tinycss2.ast import QualifiedRule, Declaration

# The CSS snippet provided as "THE FIX"
FIXED_CSS = """
#add-btn{background:#000;color:#fff;border:none;padding:10px 14px;border-radius:6px;cursor:pointer}
.todo-actions button{background:#000;border:none;color:#fff;cursor:pointer;padding:6px;border-radius:6px}
"""

# A hypothetical "pre-fix" CSS state where the colors are not black/white.
# This is crucial for reproducing the bug (i.e., showing it would fail before the fix).
# We define specific non-black/white colors to make the assertion explicit about the "buggy" state.
PRE_FIX_CSS = """
#add-btn{background:red;color:blue;border:1px solid grey}
.todo-actions button{background:green;color:yellow;font-size:14px}
/* Some other unrelated styles */
body { font-family: sans-serif; margin: 0; }
"""

def get_css_properties(css_string: str, selector: str) -> dict:
    """
    Parses a CSS string and returns a dictionary of properties for a given selector.
    Assumes simple selectors and direct property declarations within a rule.
    Handles multiple declarations for the same property by taking the last one.
    """
    properties = {}
    # parse_stylesheet returns a list of tokens, which can include rules, comments, etc.
    stylesheet = parse_stylesheet(css_string, skip_comments=True, skip_whitespace=True)

    for rule in stylesheet:
        # We are interested in QualifiedRule (CSS rules with a selector and declarations)
        if isinstance(rule, QualifiedRule):
            # Extract selector tokens and join them to form the selector string
            # tinycss2.ast.Token.serialize() converts the token back to its string representation
            rule_selector = "".join(token.serialize() for token in rule.prelude).strip()

            # Check if the current rule's selector matches the target selector
            if rule_selector == selector:
                # Iterate through the content tokens of the rule (declarations, comments, etc.)
                for content_token in rule.content:
                    if isinstance(content_token, Declaration):
                        prop_name = content_token.name.lower().strip()
                        # Join value tokens to get the full property value
                        prop_value = "".join(token.serialize() for token in content_token.value).strip()
                        properties[prop_name] = prop_value
    return properties

class TestButtonColorFix:

    def test_reproduce_original_bug(self):
        """
        Reproduces the original bug: button colors are NOT black/white before the fix.
        This test asserts that the 'PRE_FIX_CSS' does not contain the desired black/white
        colors for the target buttons, demonstrating the state that needed fixing.
        """
        add_btn_styles = get_css_properties(PRE_FIX_CSS, '#add-btn')
        todo_actions_btn_styles = get_css_properties(PRE_FIX_CSS, '.todo-actions button')

        # Assert that the background and color properties are NOT the fixed values
        # and are instead the 'buggy' values defined in PRE_FIX_CSS.
        assert add_btn_styles.get('background') != '#000', "Background of #add-btn should not be black before fix"
        assert add_btn_styles.get('color') != '#fff', "Color of #add-btn should not be white before fix"
        assert add_btn_styles.get('background') == 'red', "Expected #add-btn background to be red before fix"
        assert add_btn_styles.get('color') == 'blue', "Expected #add-btn color to be blue before fix"

        assert todo_actions_btn_styles.get('background') != '#000', "Background of .todo-actions button should not be black before fix"
        assert todo_actions_btn_styles.get('color') != '#fff', "Color of .todo-actions button should not be white before fix"
        assert todo_actions_btn_styles.get('background') == 'green', "Expected .todo-actions button background to be green before fix"
        assert todo_actions_btn_styles.get('color') == 'yellow', "Expected .todo-actions button color to be yellow before fix"

    def test_add_btn_color_fix_works(self):
        """
        Verifies that the #add-btn has the correct black background and white text color
        after the fix, along with other specified properties from the fix snippet.
        """
        add_btn_styles = get_css_properties(FIXED_CSS, '#add-btn')

        assert add_btn_styles.get('background') == '#000', "Fixed #add-btn background should be black"
        assert add_btn_styles.get('color') == '#fff', "Fixed #add-btn color should be white"
        assert add_btn_styles.get('border') == 'none', "Fixed #add-btn border should be 'none'"
        assert add_btn_styles.get('padding') == '10px 14px', "Fixed #add-btn padding is incorrect"
        assert add_btn_styles.get('border-radius') == '6px', "Fixed #add-btn border-radius is incorrect"
        assert add_btn_styles.get('cursor') == 'pointer', "Fixed #add-btn cursor is incorrect"

    def test_todo_actions_button_color_fix_works(self):
        """
        Verifies that the .todo-actions button has the correct black background and white text color
        after the fix, along with other specified properties from the fix snippet.
        """
        todo_actions_btn_styles = get_css_properties(FIXED_CSS, '.todo-actions button')

        assert todo_actions_btn_styles.get('background') == '#000', "Fixed .todo-actions button background should be black"
        assert todo_actions_btn_styles.get('color') == '#fff', "Fixed .todo-actions button color should be white"
        assert todo_actions_btn_styles.get('border') == 'none', "Fixed .todo-actions button border should be 'none'"
        assert todo_actions_btn_styles.get('cursor') == 'pointer', "Fixed .todo-actions button cursor is incorrect"
        assert todo_actions_btn_styles.get('padding') == '6px', "Fixed .todo-actions button padding is incorrect"
        assert todo_actions_btn_styles.get('border-radius') == '6px', "Fixed .todo-actions button border-radius is incorrect"

    def test_selector_not_found_graceful_handling(self):
        """
        Edge case: Tests that the helper function returns an empty dictionary
        when the target selector is not present in the CSS string.
        """
        css_without_selector = "body { margin: 0; } p { color: blue; }"
        styles = get_css_properties(css_without_selector, '#non-existent-selector')
        assert styles == {}, "Should return empty dict for non-existent selector"

    def test_empty_css_string_handling(self):
        """
        Edge case: Tests that the helper function returns an empty dictionary
        when provided with an empty CSS string.
        """
        styles = get_css_properties("", '#add-btn')
        assert styles == {}, "Should return empty dict for empty CSS string"
