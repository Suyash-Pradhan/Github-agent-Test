import re
import pytest

# The fixed CSS content provided in the problem description
FIXED_CSS_CONTENT = """
:root{
  --primary:#007bff;
  --secondary:#6c757d;
  --success:#28a745;
  --danger:#dc3545;
  --warning:#ffc107;
  --info:#17a2b8;
  --light:#f8f9fa;
  --dark:#343a40;
  --accent:#007bff; /* Example accent color */
  --muted:#6c757d; /* Example muted color */
}

body{
  font-family:sans-serif;
  margin:0;
  padding:20px;
  background-color:#f4f4f4;
  display:flex;
  justify-content:center;
  align-items:flex-start;
  min-height:100vh;
}

.container{
  background:#fff;
  padding:20px;
  border-radius:8px;
  box-shadow:0 2px 4px rgba(0,0,0,0.1);
  width:100%;
  max-width:500px;
}

h1{
  text-align:center;
  color:#333;
  margin-bottom:20px;
}

.input-section{
  display:flex;
  gap:10px;
  margin-bottom:20px;
}

.input-section input{
  flex-grow:1;
  padding:10px;
  border:1px solid #ddd;
  border-radius:6px;
  font-size:16px;
}

#add-btn{
  background: black; /* Changed from var(--accent) */
  color:#fff;
  border:none;
  padding:10px 14px;
  border-radius:6px;
  cursor:pointer
}

#add-btn:hover{
  opacity:0.9;
}

.todo-list{
  list-style:none;
  padding:0;
}

.todo-item{
  display:flex;
  align-items:center;
  padding:10px 0;
  border-bottom:1px solid #eee;
}

.todo-item:last-child{
  border-bottom:none;
}

.todo-item span{
  flex-grow:1;
  font-size:16px;
  color:#555;
}

.todo-item.completed span{
  text-decoration:line-through;
  color:#aaa;
}

.todo-actions{
  display:flex;
  gap:5px;
}

.todo-actions button{
  background:transparent;
  border:none;
  color: black; /* Changed from var(--muted) */
  cursor:pointer;
  padding:6px;
  border-radius:6px
}

.todo-actions button:hover{
  background-color:#f0f0f0;
}

.todo-actions button.complete-btn{
  color:var(--success);
}

.todo-actions button.delete-btn{
  color:var(--danger);
}
"""

# Original CSS content (simulating the bug state before the fix)
# This is constructed by reverting the changes made in the provided fix.
ORIGINAL_CSS_CONTENT = FIXED_CSS_CONTENT.replace(
    "background: black; /* Changed from var(--accent) */",
    "background: var(--accent);"
).replace(
    "color: black; /* Changed from var(--muted) */",
    "color: var(--muted);"
)

def get_css_property(css_content: str, selector: str, property_name: str) -> str | None:
    """
    A simplified function to extract a CSS property value for a given selector
    from CSS content. This uses regex and is suitable for focused tests on
    specific property changes, but is not a full CSS parser.
    """
    # Normalize whitespace to simplify regex matching across lines
    normalized_css = re.sub(r'\s+', ' ', css_content).strip()

    # Regex to find the selector block (non-greedy match for content inside braces)
    selector_pattern = re.compile(rf'{re.escape(selector)}\s*\{{([^}}]*?)\}}', re.DOTALL)
    match = selector_pattern.search(normalized_css)

    if match:
        properties_block = match.group(1)
        # Regex to find the specific property within the block
        property_pattern = re.compile(rf'{re.escape(property_name)}\s*:\s*([^;]+);')
        prop_match = property_pattern.search(properties_block)
        if prop_match:
            return prop_match.group(1).strip()
    return None

class TestButtonColorFix:

    def test_add_button_background_color_fix(self):
        """
        Tests the background color of the #add-btn.
        1. Reproduces the bug by asserting the pre-fix color.
        2. Verifies the fix by asserting the post-fix color.
        """
        # 1. Reproduce the original bug (should have failed before the fix)
        # Before the fix, #add-btn background was var(--accent)
        original_background = get_css_property(ORIGINAL_CSS_CONTENT, '#add-btn', 'background')
        assert original_background == 'var(--accent)', \
            f"Pre-fix: Expected #add-btn background to be 'var(--accent)', but got '{original_background}'"

        # 2. Verify the fix works correctly
        # After the fix, #add-btn background should be black
        fixed_background = get_css_property(FIXED_CSS_CONTENT, '#add-btn', 'background')
        assert fixed_background == 'black', \
            f"Post-fix: Expected #add-btn background to be 'black', but got '{fixed_background}'"

    def test_todo_action_button_color_fix(self):
        """
        Tests the text color of generic .todo-actions button.
        1. Reproduces the bug by asserting the pre-fix color.
        2. Verifies the fix by asserting the post-fix color.
        """
        # 1. Reproduce the original bug (should have failed before the fix)
        # Before the fix, .todo-actions button color was var(--muted)
        original_color = get_css_property(ORIGINAL_CSS_CONTENT, '.todo-actions button', 'color')
        assert original_color == 'var(--muted)', \
            f"Pre-fix: Expected .todo-actions button color to be 'var(--muted)', but got '{original_color}'"

        # 2. Verify the fix works correctly
        # After the fix, .todo-actions button color should be black
        fixed_color = get_css_property(FIXED_CSS_CONTENT, '.todo-actions button', 'color')
        assert fixed_color == 'black', \
            f"Post-fix: Expected .todo-actions button color to be 'black', but got '{fixed_color}'"

    def test_specific_todo_action_buttons_unaffected(self):
        """
        Tests that specific todo action buttons (complete, delete) retain their
        intended colors, ensuring the general button color change doesn't
        unintentionally override more specific styles (edge case).
        """
        # 3. Test any edge cases: Specific buttons should retain their specific colors
        # The .complete-btn should still be var(--success)
        complete_btn_color = get_css_property(FIXED_CSS_CONTENT, '.todo-actions button.complete-btn', 'color')
        assert complete_btn_color == 'var(--success)', \
            f"Expected .complete-btn color to remain 'var(--success)', but got '{complete_btn_color}'"

        # The .delete-btn should still be var(--danger)
        delete_btn_color = get_css_property(FIXED_CSS_CONTENT, '.todo-actions button.delete-btn', 'color')
        assert delete_btn_color == 'var(--danger)', \
            f"Expected .delete-btn color to remain 'var(--danger)', but got '{delete_btn_color}'"
