import os
import pytest
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError

AGENT_LABEL = None
# Example:
# AGENT_LABEL = "HexnodeXDR_windows_1.2.3.7"

DOWNLOAD_DIR = r"C:\Users\Mitsuser\Downloads"


@pytest.mark.browser_context_args(
    storage_state="playwright_auth.json",
    accept_downloads=True
)
def test_agent_package_download(auth_page: Page):

    page = auth_page

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # --- 1. Navigate to Installation page ---
    page.goto("https://releasetest0.xdr-qa.hexnode.com/install-agent")
    page.wait_for_load_state("networkidle")

    try:
        welcome_modal = page.get_by_role("dialog")
        welcome_modal.wait_for(state="visible", timeout=3000)
        welcome_modal.locator("button.MuiIconButton-root").first.click()
        welcome_modal.wait_for(state="hidden")
    except Exception:
        pass

    # --- 2. Select package row ---
    if AGENT_LABEL:
        print(f"\n[INSTALL LOGIC] Looking for package: {AGENT_LABEL}")
        package_row = page.locator("tbody tr").filter(has_text=AGENT_LABEL).first
    else:
        print("\n[INSTALL LOGIC] No label provided. Using top package row.")
        package_row = page.locator("tbody tr").first

    package_row.wait_for(state="visible", timeout=30000)

    package_name = package_row.locator("td").first.inner_text().strip()
    print(f"[INSTALL LOGIC] Selected package: {package_name}")

    download_btn = package_row.locator("button").last
    download_btn.wait_for(state="visible", timeout=10000)

    # --- 3. Click download and wait for real browser download ---
    print("[INSTALL LOGIC] Clicking download icon and waiting for download...")

    try:
        with page.expect_download(timeout=300000) as download_info:
            download_btn.click(force=True)

        download = download_info.value

    except PlaywrightTimeoutError:
        page.screenshot(
            path="reports/agent_download_timeout.png",
            full_page=True
        )
        pytest.fail(
            "Download did not start within 5 minutes. "
            "Pipeline/app inventory delay may still be pending."
        )

    # --- 4. Wait for toast and take screenshot ---
    toast = page.get_by_text("Download initiated", exact=False)
    expect(toast).to_be_visible(timeout=10000)

    page.screenshot(
        path="reports/agent_download_initiated.png",
        full_page=True
    )

    # --- 5. Save download to local Downloads folder ---
    suggested_name = download.suggested_filename
    final_download_path = os.path.join(DOWNLOAD_DIR, suggested_name)

    download.save_as(final_download_path)

    print(f"[INSTALL LOGIC] Download saved to: {final_download_path}")

    assert os.path.exists(final_download_path), (
        f"Downloaded file not found: {final_download_path}"
    )

    assert os.path.getsize(final_download_path) > 0, (
        f"Downloaded file is empty: {final_download_path}"
    )

    # --- 6. Close page/window ---
    page.close()

    print("[INSTALL LOGIC] Installation package download validated successfully.")