class IncidentLocators:
    INCIDENT_MENU = "text=Incidents"
    THREATS_TAB = "text=Threats"
    ALERTS_TAB = "text=Alerts"

    TABLE = "table"
    FILTER_BUTTON = "text=Filter"
    REFRESH_BUTTON = "button:has-text('Refresh')"
    COLUMN_CHOOSER = "text=Columns"

    EXPECTED_COLUMNS = [
        "ID",
        "Severity",
        "Threat",
        "Time",
        "Endpoint",
        "Status",
        "Assignee",
        "Process",
        "User",
        "Verdict"
    ]
