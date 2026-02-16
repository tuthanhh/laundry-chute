# laundry-chute

> **"Born in the earliest hours of the Lunar New Year, 2026."**

**laundry-chute** is a Python automation tool designed to streamline the process of acquiring charts for [AstroDX](). It handles the searching, downloading, and directory organization of chart files directly from Google Drive, ensuring they are ready to be imported into the AstroDX database without manual file management.

## Prerequisites

* [uv](https://docs.astral.sh/uv/)
* A Google Cloud Project with the **Google Drive API** and **Google Sheets API** enabled.
* `key.json` (Service Account or OAuth client) placed in the `.config` directory. The example file can be found in the `.config` directory.
* `adb` tool installed and available in your system's PATH.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tuthanhh/laundry-chute.git
cd laundry-chute
```

2. Install dependencies:
```bash
uv sync
```

3. Run the application:
```bash
uv run laundry-chute
```

## To-Do / Roadmap

* [ ] Add CLI arguments for easier bulk downloading.
* [ ] Write proper documentation (current status: *pending motivation*).

---

*Happy Lunar New Year! 🧧*
