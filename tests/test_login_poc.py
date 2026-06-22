import re
import pyotp 
from playwright.sync_api import Page, expect, BrowserContext

def test_xdr_positive_login_and_portal_navigation(page: Page, context: BrowserContext):
    # --- STEP 1 & 2: Navigate and Enter Username ---
    page.goto("https://accounts-staging.hexnode.com/login/")
    
    # Locate by input type since there are no placeholders
    email_input = page.locator("input[type='email']")
    email_input.fill("yageshwaran.saravanan@mitsogo.com")
    
    # --- STEP 3: Press Enter to view password ---
    email_input.press("Enter")
    
    # Wait for the password field to become visible, then fill it
    password_input = page.locator("input[type='password']")
    password_input.wait_for(state="visible")
    password_input.fill("Tryhard1!")
    password_input.press("Enter")
    
    # --- STEP 4: Handle 6-Digit OTP with Live Generation ---
    # Wait for the exact title div to ensure the MFA page loaded
    page.locator(".hex-title").wait_for(state="visible", timeout=15000)
    
    # Locate the first verification code input specifically by its name attribute
    first_otp_box = page.locator('input[name="verification-code"]').first
    first_otp_box.wait_for(state="visible")
    
    # INSERT YOUR ACTUAL SECRET KEY STRING HERE
    TOTP_SECRET = "NGA2Y6Y3XWV5HR7JTZJB5GW7UKI44AUGQI5LIDFRRYIH62P6DMCA" 
    
    totp = pyotp.TOTP(TOTP_SECRET)
    current_otp = totp.now()
    
    print(f"Generated OTP: {current_otp}")
    
    # Click the first box to focus
    first_otp_box.click() 
    
    # Type and tab through the 6 boxes
    for digit in current_otp:
        page.keyboard.type(digit)
        page.keyboard.press("Tab")
        
    # Using the exact button ID from your DOM
    verify_btn = page.locator('#verify-code')
    if verify_btn.is_visible():
        verify_btn.click()

    # --- STEP 5: Redirect to Hexnode ---
    # Instead of looking for text, we wait for the exact sidebar element 
    # with the title attribute shown in your DOM inspector
    my_portals_btn = page.locator('div[title="My Portals"]')
    expect(my_portals_btn).to_be_visible(timeout=15000)

    # --- STEP 6: Navigate to My Portals & Select Target Portal ---
    my_portals_btn.click()
    
    # Click the target portal
    page.get_by_text("https://zeqmad.xdr-qa.hexnode.com", exact=True).click()
    
    # Wait for the current page to finish loading the new URL
    page.wait_for_load_state("networkidle")

    # --- FINAL STEP: Validation ---
    # Strictly validate the URL and let the test finish (Pytest will close the browser automatically)
    expect(page).to_have_url(re.compile(r".*zeqmad\.xdr-qa\.hexnode\.com.*"), timeout=15000)
    # NEW:Save the authentication state (cookies and local storage)
    context.storage_state(path="playwright_auth.json")