import pytest
from playwright.sync_api import Page, expect

@pytest.mark.browser_context_args(storage_state="playwright_auth.json")
def test_smart_uninstall_flow(auth_page: Page):
    
    page = auth_page
    
    # --- 1. Navigate & Bypass Login ---
    page.goto("https://zeqmad.xdr-qa.hexnode.com/endpoints/all")
    page.wait_for_load_state("networkidle")

    try:
        welcome_modal = page.get_by_role("dialog")
        welcome_modal.wait_for(state="visible", timeout=3000)
        close_btn = welcome_modal.locator("button.MuiIconButton-root").first
        close_btn.click()
        welcome_modal.wait_for(state="hidden")
    except Exception:
        pass

    # --- 2. Select the Specific Endpoint ---
    print("\n[SMART LOGIC] Locating endpoint 'DESKTOP-E1KLJIC'...")
    target_endpoint = page.get_by_text("DESKTOP-E1KLJIC", exact=True).first
    target_endpoint.wait_for(state="visible", timeout=15000)
    target_endpoint.click()
    page.wait_for_load_state("networkidle")

    # --- 3. Navigate to Action History ---
    action_tab = page.get_by_text("Action History", exact=True)
    action_tab.wait_for(state="visible", timeout=10000)
    action_tab.click()
    page.wait_for_load_state("networkidle")

    # --- 4. State Capture ---
    top_row = page.locator("tbody tr").first
    old_row_text = top_row.inner_text() if top_row.is_visible() else "EMPTY"

    # --- 5. Trigger Action ---
    print("\n[SMART LOGIC] Endpoint selected. Triggering action now...")
    page.get_by_role("button", name="Actions").click()
    page.wait_for_timeout(500) 
    page.get_by_text("Uninstall Agent", exact=True).click()
    page.get_by_role("button", name="Confirm").click()
    
    expect(page.get_by_text("Action execution initiated")).to_be_visible(timeout=5000)

    # ==========================================
    # --- 6. The Unified Polling Engine ---
    # ==========================================
    refresh_button = page.locator("button:right-of(:text('Last updated'))").first
    success_achieved = False
    
    for attempt in range(40):
        print(f"\n[SMART LOGIC] Polling (Attempt {attempt + 1}/40): Clicking refresh...")
        refresh_button.click(force=True)
        
        # Give the table 2 seconds to fetch the data and update the DOM
        page.wait_for_timeout(2000)
        
        # 1. Check if the backend has generated the new row yet
        if top_row.inner_text() == old_row_text:
            print("  -> Still seeing old action. Waiting for backend...")
            page.wait_for_timeout(3000)
            continue # Skip to the next loop iteration to click refresh again
            
        # 2. If it's a new row, check the Status column (3rd column = index 2)
        current_status = top_row.locator("td").nth(2).inner_text()
        print(f"  -> New action found! Status is '{current_status}'")
        
        if "Success" in current_status:
            success_achieved = True
            break
        elif "Failed" in current_status:
            print(f"\n[SMART LOGIC] Server aborted! Status changed to '{current_status}'.")
            break
            
        # If it's "Pending" or "In Progress", wait 3 seconds before the next refresh
        page.wait_for_timeout(3000)

    # --- 7. Final Validation ---
    if success_achieved:
        print("\n[SMART LOGIC] Validation complete. Uninstall Successful!")
        expect(top_row.locator("td").nth(2)).to_have_text("Success", timeout=5000)
        page.screenshot(path="reports/08_final_uninstall_success.png")
    else:
        print("\n[SMART LOGIC] Uninstall not yet success, check manually")
        page.screenshot(path="reports/09_uninstall_timeout_manual_check.png")
        pytest.fail("Uninstall did not reach 'Success' within the expected timeframe.")