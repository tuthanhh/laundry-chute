from dataclasses import dataclass
from pathlib import Path

import gspread
from google.oauth2 import service_account


@dataclass
class Chart:
    row_index: int
    name: str
    version: str
    type: str


class SheetParser:
    def __init__(self):
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        self.client = None

    def connect(self, key_file: str):
        if Path(key_file).exists():
            credentials = service_account.Credentials.from_service_account_file(
                key_file, scopes=self.scopes
            )
            self.client = gspread.authorize(credentials)
        else:
            raise FileNotFoundError(f"Key file not found: {key_file}")

    def fetch_charts(self, sheet_url: str, worksheet_name: str) -> list[Chart]:
        if self.client is None:
            raise ValueError("Client not connected, please call connect() first")

        charts = []
        raw_sheet = (
            self.client.open_by_url(sheet_url)
            .worksheet(worksheet_name)
            .get_all_records()
        )

        for row_index, row in enumerate(raw_sheet):
            print(row)
            charts.append(Chart(row_index, str(row["Song Name"]), str(row["Version"]), str(row["STD/DX"])))

        return charts
