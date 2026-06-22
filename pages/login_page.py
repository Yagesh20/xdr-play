from playwright.sync_api import Page, expect
from config.settings import BASE_URL, EMAIL, PASSWORD
from utils.otp_generator import get_fresh_otp


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

    def login(self):
        self.page.goto(BASE_URL)

        # Email
        self.page.locator("input[name='email']").fill(EMAIL)
        self.page.locator("input[name='email']").press("Enter")

        # Password
        self.page.wait_for_selector("input[type='password']", timeout=15000)
        self.page.locator("input[type='password']").fill(PASSWORD)
        self.page.locator("input[type='password']").press("Enter")

        # OTP
        self.page.wait_for_selector(
            "input[name='verification-code']",
            timeout=15000
        )

        self.enter_totp_and_submit()

        # If invalid code appears, retry once with next fresh OTP
        if self.page.locator("text=Invalid code").is_visible(timeout=3000):
            print("Invalid OTP detected. Retrying with next OTP...")
            self.clear_otp_fields()
            self.enter_totp_and_submit()

        self.page.wait_for_timeout(5000)

        print("Current URL:", self.page.url)

    def enter_totp_and_submit(self):
        otp_code = get_fresh_otp()
        print("Generated OTP:", otp_code)

        otp_inputs = self.page.locator("input[name='verification-code']")

        otp_inputs.first.click()

        for digit in otp_code:
            self.page.keyboard.type(digit)
            self.page.keyboard.press("Tab")

        self.page.locator("button[type='submit']").click()

    def clear_otp_fields(self):
        otp_inputs = self.page.locator("input[name='verification-code']")

        for i in range(6):
            otp_inputs.nth(i).evaluate(
                "element => element.value = ''"
            )

        self.page.wait_for_timeout(1000)