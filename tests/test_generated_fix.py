import pytest
from playwright.sync_api import Page, expect

# Assuming the app is running on localhost:3000 during tests
BASE_URL = "http://localhost:3000"

def test_filter_buttons_have_rounded_corners(page: Page):
    """
    Verifies that the filter buttons contain the 'rounded-full' class.
    This confirms the fix for the square corners issue.
    """
    page.goto(BASE_URL)
    
    # Select all filter buttons in the sidebar
    # The filter buttons are identified by the container with the specific layout
    filter_buttons = page.locator("div.overflow-x-auto button")
    
    # Ensure buttons exist
    expect(filter_buttons.first).to_be_visible()
    
    # Verify that every button has the 'rounded-full' class
    count = filter_buttons.count()
    for i in range(count):
        button = filter_buttons.nth(i)
        # Check for the Tailwind class that provides rounded corners
        expect(button).to_have_class(lambda c: "rounded-full" in c)

def test_filter_buttons_maintain_styling_on_selection(page: Page):
    """
    Verifies that the rounded corners are preserved even when the 
    button state changes (e.g., when selected).
    """
    page.goto(BASE_URL)
    
    # Click the 'orange' filter button
    orange_filter = page.locator("button", has_text="Orange")
    orange_filter.click()
    
    # Verify it is selected (has primary background) and still rounded
    expect(orange_filter).to_have_class(lambda c: "rounded-full" in c and "bg-primary" in c)

def test_filter_buttons_edge_case_all_tags_rendered(page: Page):
    """
    Verifies that all expected filter tags are rendered and all are rounded,
    ensuring no specific tag was missed in the styling update.
    """
    page.goto(BASE_URL)
    
    expected_tags = ['All', 'None', 'Orange', 'Pink', 'Violet', 'Emerald']
    
    for tag_name in expected_tags:
        button = page.locator("button", has_text=tag_name)
        expect(button).to_be_visible()
        expect(button).to_have_class(lambda c: "rounded-full" in c)
