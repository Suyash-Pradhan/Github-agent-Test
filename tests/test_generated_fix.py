import pytest
from playwright.sync_api import Page
import os
import tempfile

# Helper function to create a temporary HTML file with embedded CSS
def create_html_file(css_content: str) -> str:
    """
    Creates a temporary HTML file with the given CSS content embedded in a <style> tag.
    Returns the path to the created file.
    """
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo App Test</title>
        <style id="test-style">
            {css_content}
        </style>
    </head>
    <body>
        <div class="app">
            <h1>My Todos</h1>
            <div class="todo-list">
                <div class="todo-item">
                    <div class="left">
                        <input type="checkbox">
                        <span class="text">Buy groceries</span>
                    </div>
                    <div class="todo-actions">
                        <button class="delete-btn">Delete</button>
                    </div>
                </div>
                <div class="todo-item completed">
                    <div class="left">
                        <input type="checkbox" checked>
                        <span class="text">Walk the dog</span>
                    </div>
                    <div class="todo-actions">
                        <button class="edit-btn">Edit</button>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    # Create a temporary file
    fd, path = tempfile.mkstemp(suffix=".html")
    with os.fdopen(fd, 'w') as tmp:
        tmp.write(html_template)
    return path

# Define the CSS content for pre-fix and post-fix states
# The pre-fix CSS assumes the button color was previously set to the accent variable,
# which is a common pattern and explains why it wouldn't be black by default.
PRE_FIX_CSS = """
:root{--bg:#f7f7fb;--card:#ffffff;--accent:#5b8def;--muted:#6b7280}
*{box-sizing:border-box}
body{font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);margin:0;display:flex;align-items:center;justify-content:center;height:100vh}
.app{width:100%;max-width:520px;padding:24px}
h1{text-align:center;margin:0 0 16px}
.todo-form{display:flex;gap:8px;margin-bottom:16px}
#todo-input{flex:1;padding:10px;border:1px solid #e5e7eb;border-radius:6px}
#add-btn{background:var(--accent);color:#fff;border:none;padding:10px 14px;border-radius:6px;cursor:pointer}
.todo-list{list-style:none;padding:0;margin:0}
.todo-item{background:var(--card);display:flex;align-items:center;justify-content:space-between;padding:10px;border-radius:8px;margin-bottom:8px;box-shadow:0 1px 2px rgba(16,24,40,0.04)}
.todo-item .left{display:flex;gap:12px;align-items:center}
.todo-item input[type=checkbox]{width:18px;height:18px}
.todo-item.completed .text{opacity:0.6;text-decoration:line-through}
.todo-actions button{background:transparent;border:none;color:var(--accent);cursor:pointer;padding:6px;border-radius:6px} /* THE BUGGED LINE: color was var(--accent) */
.empty{color:var(--muted);text-align:center;padding:18px}
"""

# The provided fixed CSS
POST_FIX_CSS = """
:root{--bg:#f7f7fb;--card:#ffffff;--accent:#5b8def;--muted:#6b7280}
*{box-sizing:border-box}
body{font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:var(--bg);margin:0;display:flex;align-items:center;justify-content:center;height:100vh}
.app{width:100%;max-width:520px;padding:24px}
h1{text-align:center;margin:0 0 16px}
.todo-form{display:flex;gap:8px;margin-bottom:16px}
#todo-input{flex:1;padding:10px;border:1px solid #e5e7eb;border-radius:6px}
#add-btn{background:var(--accent);color:#fff;border:none;padding:10px 14px;border-radius:6px;cursor:pointer}
.todo-list{list-style:none;padding:0;margin:0}
.todo-item{background:var(--card);display:flex;align-items:center;justify-content:space-between;padding:10px;border-radius:8px;margin-bottom:8px;box-shadow:0 1px 2px rgba(16,24,40,0.04)}
.todo-item .left{display:flex;gap:12px;align-items:center}
.todo-item input[type=checkbox]{width:18px;height:18px}
.todo-item.completed .text{opacity:0.6;text-decoration:line-through}
.todo-actions button{background:transparent;border:none;color:black;cursor:pointer;padding:6px;border-radius:6px} /* THE FIXED LINE: color is black */
.empty{color:var(--muted);text-align:center;padding:18px}
"""

# Expected colors in RGB format as returned by getComputedStyle
ACCENT_COLOR_RGB = "rgb(91, 141, 239)" # Corresponds to #5b8def
BLACK_COLOR_RGB = "rgb(0, 0, 0)"

@pytest.fixture(scope="module")
def html_file_pre_fix():
    """Fixture to create and clean up a temporary HTML file with pre-fix CSS."""
    path = create_html_file(PRE_FIX_CSS)
    yield path
    os.remove(path)

@pytest.fixture(scope="module")
def html_file_post_fix():
    """Fixture to create and clean up a temporary HTML file with post-fix CSS."""
    path = create_html_file(POST_FIX_CSS)
    yield path
    os.remove(path)

def get_computed_color(page: Page, selector: str) -> str:
    """Helper to get the computed color of an element using Playwright."""
    return page.locator(selector).evaluate("el => getComputedStyle(el).color")

def test_button_color_reproduces_bug_pre_fix(page: Page, html_file_pre_fix: str):
    """
    Test 1: Reproduces the original bug.
    Verifies that before the fix, buttons within '.todo-actions' had the accent color.
    This test should FAIL if the fix (setting color to black) was already applied.
    """
    page.goto(f"file://{html_file_pre_fix}")

    # Check the color of the delete button
    delete_button_color = get_computed_color(page, ".todo-actions .delete-btn")
    assert delete_button_color == ACCENT_COLOR_RGB, \
        f"BUG REPRODUCTION FAILED: Expected pre-fix button color to be {ACCENT_COLOR_RGB}, but got {delete_button_color}. " \
        "This indicates the button might already be black or a different color."

    # Check the color of the edit button (another button in todo-actions)
    edit_button_color = get_computed_color(page, ".todo-actions .edit-btn")
    assert edit_button_color == ACCENT_COLOR_RGB, \
        f"BUG REPRODUCTION FAILED: Expected pre-fix button color to be {ACCENT_COLOR_RGB}, but got {edit_button_color}. " \
        "This indicates the button might already be black or a different color."

def test_button_color_verifies_fix_post_fix(page: Page, html_file_post_fix: str):
    """
    Test 2: Verifies the fix works correctly.
    Checks that after the fix, buttons within '.todo-actions' have the color black.
    This test should PASS after the fix is applied.
    """
    page.goto(f"file://{html_file_post_fix}")

    # Check the color of the delete button
    delete_button_color = get_computed_color(page, ".todo-actions .delete-btn")
    assert delete_button_color == BLACK_COLOR_RGB, \
        f"FIX VERIFICATION FAILED: Expected post-fix button color to be {BLACK_COLOR_RGB}, but got {delete_button_color}."

    # Check the color of the edit button (another button in todo-actions)
    edit_button_color = get_computed_color(page, ".todo-actions .edit-btn")
    assert edit_button_color == BLACK_COLOR_RGB, \
        f"FIX VERIFICATION FAILED: Expected post-fix button color to be {BLACK_COLOR_RGB}, but got {edit_button_color}."

def test_button_color_edge_case_multiple_buttons_post_fix(page: Page, html_file_post_fix: str):
    """
    Test 3: Edge case - Verifies the fix applies to all relevant buttons.
    Ensures that all buttons within the '.todo-actions' container correctly adopt the black color
    after the fix, confirming the CSS selector's intended broad application.
    """
    page.goto(f"file://{html_file_post_fix}")

    # Get all buttons within .todo-actions
    buttons = page.locator(".todo-actions button").all()
    assert len(buttons) == 2, "Expected two buttons in .todo-actions for this test scenario."

    for i, button_locator in enumerate(buttons):
        button_color = button_locator.evaluate("el => getComputedStyle(el).color")
        assert button_color == BLACK_COLOR_RGB, \
            f"EDGE CASE FAILED: Expected button {i+1} color to be {BLACK_COLOR_RGB}, but got {button_color}. " \
            "This indicates the fix might not be applying to all relevant buttons."
