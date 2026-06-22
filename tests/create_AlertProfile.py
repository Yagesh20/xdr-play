import pytest
from playwright.sync_api import Page, expect

PROFILE_NAME = "QA Auto Alert Profile"

EVENT_CATEGORY = "Windows"
EVENT_SUB_CATEGORY = "File"
EVENT_NAME = "File Created"

SEVERITIES = ["Low", "Medium", "High", "Critical"]

TECHNICIAN_NAME = "yagesh"


@pytest.mark.browser_context_args(storage_state="playwright_auth.json")
def test_create_alert_profile(auth_page: Page):
    page = auth_page

    # --- 1. Navigate to Alert Profiles ---
    page.goto("https://zeqmad.xdr-qa.hexnode.com/settings/alert-profiles")
    page.wait_for_load_state("networkidle")

    try:
        welcome_modal = page.get_by_role("dialog")
        welcome_modal.wait_for(state="visible", timeout=3000)
        welcome_modal.locator("button.MuiIconButton-root").first.click()
        welcome_modal.wait_for(state="hidden")
    except Exception:
        pass

    # --- 2. Click New ---
    page.get_by_role("button", name="New").click()
    page.wait_for_load_state("networkidle")

    expect(page.get_by_text("New Alert Profile")).to_be_visible(timeout=10000)

    # --- 3. Event step ---
    page.get_by_role("button", name="Add New Event").click()

    event_modal = page.get_by_role("dialog")
    expect(event_modal).to_be_visible(timeout=10000)

    event_modal.get_by_text(EVENT_CATEGORY, exact=True).click()
    event_modal.get_by_text(EVENT_SUB_CATEGORY, exact=True).click()
    event_modal.get_by_text(EVENT_NAME, exact=True).click()

    event_modal.get_by_role("button", name="Add").click()

    # --- 4. Add filter severity ---
    page.get_by_role("button", name="Add Filter").click()

    filter_modal = page.get_by_role("dialog")
    expect(filter_modal).to_be_visible(timeout=10000)

    filter_modal.get_by_text("Severity", exact=True).click()
    filter_modal.get_by_text("In", exact=True).click()

    for severity in SEVERITIES:
        filter_modal.get_by_text(severity, exact=True).click()

    filter_modal.get_by_role("button", name="Add").click()

    page.get_by_role("button", name="Next").click()

    # --- 5. Source step ---
    expect(page.get_by_text("Source")).to_be_visible(timeout=10000)

    page.get_by_role("button", name="Add Sources").click()

    source_modal = page.get_by_role("dialog")
    expect(source_modal).to_be_visible(timeout=10000)

    source_modal.get_by_text(TECHNICIAN_NAME, exact=False).first.click()
    source_modal.get_by_role("button", name="Add").click()

    page.get_by_role("button", name="Next").click()

    # --- 6. Schedule step ---
    expect(page.get_by_text("Schedule")).to_be_visible(timeout=10000)

    page.locator("input").first.click()
    page.get_by_text("Immediately", exact=True).click()

    page.get_by_role("button", name="Next").click()

    # --- 7. Channels step ---
    expect(page.get_by_text("Channels")).to_be_visible(timeout=10000)

    email_box = page.locator("textarea").first
    email_box.fill(
        "Detection $DetectionName rule saved with severity $DetectionSeverity "
        "was found in $DetectionSourceName endpoint."
    )

    page.get_by_role("button", name="Next").click()

    # --- 8. Review step ---
    expect(page.get_by_text("Review")).to_be_visible(timeout=10000)

    page.locator("input[name='name'], input[placeholder*='Name']").first.fill(PROFILE_NAME)

    page.screenshot(
        path="reports/alert_profile_review_before_create.png",
        full_page=True
    )

    page.get_by_role("button", name="Save").click()

    expect(page.get_by_text("Alert profile", exact=False)).to_be_visible(timeout=15000)

    page.screenshot(
        path="reports/alert_profile_created.png",
        full_page=True
    )

    page.close()