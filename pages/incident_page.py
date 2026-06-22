from playwright.sync_api import expect
from locators.incident_locators import IncidentLocators


class IncidentPage:

    def __init__(self, page):
        self.page = page

    def open_incidents_page(self):
        self.page.click(IncidentLocators.INCIDENT_MENU)
        expect(self.page.locator(IncidentLocators.THREATS_TAB)).to_be_visible()

    def verify_incident_page_loaded(self):
        expect(self.page.locator(IncidentLocators.THREATS_TAB)).to_be_visible()
        expect(self.page.locator(IncidentLocators.ALERTS_TAB)).to_be_visible()

    def verify_columns_present(self):
        for column in IncidentLocators.EXPECTED_COLUMNS:
            expect(self.page.locator(f"text={column}")).to_be_visible()

    def verify_basic_actions_present(self):
        expect(self.page.locator(IncidentLocators.FILTER_BUTTON)).to_be_visible()
        expect(self.page.locator(IncidentLocators.REFRESH_BUTTON)).to_be_visible()
        expect(self.page.locator(IncidentLocators.COLUMN_CHOOSER)).to_be_visible()
        