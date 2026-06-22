import pytest
import pyotp
import re
from playwright.sync_api import Page, expect

@pytest.fixture
def auth_page(page: Page, context):
    """
    Checks if session is valid. If redirected to login, automatically re-authenticates.
    """
    # 1. Attempt to go directly to the dashboard
    page.goto("https://zeqmad.xdr-qa.hexnode.com/dashboards")
    page.wait_for_load_state("networkidle")

    # 2. Check if the app redirected us to the login screen
    if "login" in page.url:
        print("\n[AUTH ENGINE] Session expired. Executing auto-login...")
        
        # --- Your exact login script logic ---
        email_input = page.locator("input[type='email']")
        email_input.fill("yageshwaran.saravanan@mitsogo.com")
        email_input.press("Enter")
        
        password_input = page.locator("input[type='password']")
        password_input.wait_for(state="visible")
        password_input.fill("Tryhard1!")
        password_input.press("Enter")
        
        # MFA Handle
        page.locator(".hex-title").wait_for(state="visible", timeout=15000)
        first_otp_box = page.locator('input[name="verification-code"]').first
        first_otp_box.wait_for(state="visible")
        
        TOTP_SECRET = "NGA2Y6Y3XWV5HR7JTZJB5GW7UKI44AUGQI5LIDFRRYIH62P6DMCA" # Put your secret here
        totp = pyotp.TOTP(TOTP_SECRET)
        current_otp = totp.now()
        
        first_otp_box.click()
        for digit in current_otp:
            page.keyboard.type(digit)
            page.keyboard.press("Tab")
            
        # ... OTP entry ...
        verify_btn = page.locator('#verify-code')
        if verify_btn.is_visible():
            verify_btn.click()

        # ==========================================
        # --- NEW DEEP LINK HANDLING ---
        # ==========================================
        print("\n[AUTH ENGINE] Waiting for SSO auto-redirect to XDR portal...")
        
        # Wait for the URL to change to our specific portal (max 20 seconds)
        page.wait_for_url(re.compile(r".*zeqmad\.xdr-qa\.hexnode\.com.*"), timeout=20000)
        page.wait_for_load_state("networkidle")
        
        # 3. Save the fresh session state
        context.storage_state(path="playwright_auth.json")
        print("\n[AUTH ENGINE] New session saved. Resuming test...")

    # 4. Hand the authenticated page over to the actual test
    yield page