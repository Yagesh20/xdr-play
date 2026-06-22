import pytest
from playwright.sync_api import Page, expect

@pytest.mark.browser_context_args(storage_state="playwright_auth.json")
def test_alert_profiles_navigation_and_table(page: Page):
    # --- 1. Navigate and Bypass Login ---
    # Start at the main dashboard
    page.goto("https://zeqmad.xdr-qa.hexnode.com/dashboards")
    page.wait_for_load_state("networkidle")

    # Handle the "Welcome Aboard" modal just in case it appears
    try:
        welcome_modal = page.get_by_role("dialog")
        welcome_modal.wait_for(state="visible", timeout=3000)
        close_btn = welcome_modal.locator("button.MuiIconButton-root").first
        close_btn.click()
        welcome_modal.wait_for(state="hidden")
    except Exception:
        pass

    # --- 2. Navigate to Settings -> Alert Profiles ---
    # Click the Settings tab in the top navigation bar
    page.get_by_text("Settings", exact=True).click()
    page.wait_for_load_state("networkidle")

    # Click 'Alert Profiles' in the left sidebar
    # Using exact=True ensures we don't accidentally click something else containing those words
    page.get_by_text("Alert Profiles", exact=True).first.click()
    page.wait_for_load_state("networkidle")

    # --- 3. Validate Page Load ---
    # Using get_by_text instead of get_by_role catches it even if it's a styled <div> or <span>.
    # We use .first in case the word "New" appears in your table data below.
    new_btn = page.get_by_text("New", exact=True).first
    expect(new_btn).to_be_visible(timeout=10000)
    
    # Ensure the URL updated correctly
    expect(page).to_have_url(re.compile(r".*zeqmad\.xdr-qa\.hexnode\.com/alert-profiles.*"))
    
    # --- 4. Validate Table Columns ---
    # List of column headers from your second screenshot
    expected_columns = ["Name", "Description", "Created Time", "Status"]
    
    for column in expected_columns:
        # Use .first to avoid strict mode errors if the text appears elsewhere
        header = page.get_by_text(column, exact=True).first
        expect(header).to_be_visible()

    # --- 5. Final Screenshot ---
    page.screenshot(path="reports/03_alert_profiles_validated.png")