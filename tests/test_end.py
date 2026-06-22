import pytest
from playwright.sync_api import Page, expect

@pytest.mark.browser_context_args(storage_state="playwright_auth.json")
def test_action_history_polling_only(page: Page):
    
    # --- 1. Navigate to Endpoints ---
    page.goto("https://zeqmad.xdr-qa.hexnode.com/endpoints/all")
    page.wait_for_load_state("networkidle")

    # Handle the "Welcome Aboard" modal if it appears
    try:
        welcome_modal = page.get_by_role("dialog")
        welcome_modal.wait_for(state="visible", timeout=3000)
        close_btn = welcome_modal.locator("button.MuiIconButton-root").first
        close_btn.click()
        welcome_modal.wait_for(state="hidden")
    except Exception:
        pass

    # --- 2. Select the Specific Endpoint ---
    page.get_by_text("yagesh-desktop", exact=True).first.click()
    page.wait_for_load_state("networkidle")

    # --- 3. Navigate to Action History Tab ---
    page.get_by_text("Action History", exact=True).click()
    page.wait_for_load_state("networkidle")

    # ==========================================
    # --- 4. TRIGGER ACTION (COMMENTED OUT) ---
    # page.get_by_role("button", name="Actions").click()
    # page.wait_for_timeout(500)
    # page.get_by_text("Uninstall Agent", exact=True).click()
    # page.get_by_role("button", name="Confirm").click()
    # expect(page.get_by_text("Action execution initiated")).to_be_visible(timeout=5000)
    # ==========================================

    # Isolate the exact table row for the most recent Uninstall action
    action_row = page.locator("tr").filter(has_text="UninstallEndpoint").first

    # ==========================================
    # --- 5. "IN PROGRESS" CHECK (COMMENTED OUT) ---
    # expect(action_row).to_contain_text("In Progress", timeout=15000)
    # page.screenshot(path="reports/04_uninstall_in_progress.png")
    # ==========================================

    # --- 6. The Polling Loop Test ---
    # Use a layout selector: Find a button visually to the right of the 'Last updated' text
    refresh_button = page.locator("button:right-of(:text('Last updated'))").first
    
    for _ in range(10):
        if action_row.locator("text='Success'").is_visible():
            print("\n[SMART LOGIC] Status is Success! Validation complete.")
            break
            
        print("\n[SMART LOGIC] Polling: Clicking refresh...")
        refresh_button.click()
        page.wait_for_timeout(3000)

    # --- 7. Final Validation & Screenshot ---
    expect(action_row).to_contain_text("Success", timeout=5000)
    page.screenshot(path="reports/06_polling_test_success.png")