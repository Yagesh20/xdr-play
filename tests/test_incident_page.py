import pytest
from playwright.sync_api import Page, expect

@pytest.mark.browser_context_args(storage_state="playwright_auth.json")
def test_create_new_incident_and_validate_table(page: Page):
    # Navigate directly to the target portal
    page.goto("https://zeqmad.xdr-qa.hexnode.com/dashboards")
    page.wait_for_load_state("networkidle")
    
    # --- 1. Handle the "Welcome Aboard" Modal ---
    try:
        # Isolate the modal using the exact role
        welcome_modal = page.get_by_role("dialog")
        welcome_modal.wait_for(state="visible", timeout=5000)
        
        # Target the top-right 'X' button. 
        # In Material UI, this is an icon button. We take the .first() one found in the dialog.
        close_btn = welcome_modal.locator("button.MuiIconButton-root").first
        close_btn.click()
        
        # CRITICAL: Wait for the modal to completely disappear before moving on
        welcome_modal.wait_for(state="hidden")
    except Exception:
        pass # If the modal doesn't appear on subsequent runs, safely continue

    # --- 2. Validate Dashboard & Screenshot ---
    # Use get_by_text instead of role, and .first to avoid strict mode errors
    dashboard_title = page.get_by_text("Dashboard", exact=True).first
    expect(dashboard_title).to_be_visible(timeout=10000)
    
    # Take the first screenshot and save it to your reports folder
    page.screenshot(path="reports/01_dashboard_clean.png")

    # --- 3. Navigate to Incidents Tab ---
    # Click the Incidents menu item from the top navigation
    page.get_by_text("Incidents", exact=True).click()
    page.wait_for_load_state("networkidle")

    # Ensure the Incidents page loaded by checking the title
    expect(page.get_by_text("All Threats", exact=True).first).to_be_visible(timeout=5000)

    # --- 4. Validate Table Columns ---
    # A list of the exact column names from your screenshot
    expected_columns = ["ID", "Severity", "Threat", "Target", "Status", "Assignee"]
    
    for column_name in expected_columns:
        # We loop through each name and assert it is visible on the screen.
        # We use .first in case the word (like "High" or "Open") appears in the data rows as well.
        column_element = page.get_by_text(column_name).first
        expect(column_element).to_be_visible()

    # --- 5. Final Validation Screenshot ---
    page.screenshot(path="reports/02_incidents_table_validated.png")