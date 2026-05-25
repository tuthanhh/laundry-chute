# laundry-chute

> **"Born in the earliest hours of the Lunar New Year, 2026."**

**laundry-chute** is a Python automation tool that streamlines acquiring charts for [AstroDX](https://www.astrodx.com/). It searches, downloads, and organizes chart files directly from Google Drive, then pushes them to your phone — ready to play without manual file management.

## Features

* Reads a chart list from a Google Sheet
* Downloads matching folders from Google Drive (skip-if-exists by file size)
* Pushes packages to Android (via ADB) or iOS (via ifuse)
* Filter by chart type (STD/DX)
* Run download phase and push phase independently
* All settings driven by a single TOML config file

## Prerequisites

* [uv](https://docs.astral.sh/uv/)
* Python 3.13+
* A Google Cloud Project with the **Google Drive API** and **Google Sheets API** enabled
* Service account `key.json` placed at `.config/key.json` (see `.config/key-example.json` for the expected structure)

### Android target

* `adb` installed and on your `PATH` (part of [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools))
* USB Debugging enabled on the device, device authorized for your machine

### iOS target

Requires [libimobiledevice](https://libimobiledevice.org/) and [ifuse](https://github.com/libimobiledevice/ifuse). Install:

* **Debian / Ubuntu**: `sudo apt install ifuse libimobiledevice-utils`
* **Fedora**: `sudo dnf install ifuse libimobiledevice-utils`
* **Arch**: `sudo pacman -S ifuse libimobiledevice`
* **macOS**: `brew install ifuse libimobiledevice` (requires [macFUSE](https://osxfuse.github.io/))

Device must be paired and trusted (`idevicepair pair` if needed).

## Installation

```bash
git clone https://github.com/tuthanhh/laundry-chute.git
cd laundry-chute
uv sync
```

## Usage

Copy the example config and edit:

```bash
cp .config/settings-example.toml .config/settings.toml
```

Run the full pipeline (download + push):

```bash
uv run laundry-chute
```

### CLI flags

| Flag | Description |
|------|-------------|
| `--config PATH` | Config file path (default: `.config/settings.toml`) |
| `--type STD\|DX` | Filter charts by type. Omit to download all |
| `--os android\|ios` | Target device. Default: `android` |
| `--download-only` | Fetch from Drive, skip device push |
| `--push-only` | Skip Drive, push existing folders in `download_dir` |

Examples:

```bash
uv run laundry-chute --type DX --os ios
uv run laundry-chute --download-only
uv run laundry-chute --push-only --config alt.toml
```

### Config file

Edit `.config/settings.toml`:

```toml
key_file = ".config/key.json"
root_id = "<google-drive-root-folder-id>"
sheet_url = "<google-sheet-url>"
worksheet = "<worksheet-name>"
download_dir = "downloads"

[android]
destination = "/sdcard/Android/data/com.Reflektone.AstroDX/files/levels/"

[ios]
id = "<ios-bundle-id>"
mount_point = "./mnt"
```

## Development

```bash
uv sync               # install
uv run laundry-chute  # run
uv run pytest         # run tests (WIP)
```

> ⚠️ Tests are WIP — currently integration-only, hit live Google APIs, and require a real `.config/key.json`.

## Roadmap

* [ ] Add CLI arguments for easier bulk downloading
  * [x] Choosing a specific chart type
  * [ ] Choosing date range
  * [x] Choosing operating system (iOS/Android)
  * [ ] Specifying input spreadsheet
  * [x] Adding option for downloading only / file transfers only
* [ ] Retry logic for failed file transfers due to missing permissions
* [x] Using a configuration file for settings
* [ ] Write proper documentation (current status: *pending motivation*)
* [ ] Using DBMS for handling file transfers

## License

[MIT](LICENSE) — free to use, modify, distribute. Personal project, no contributions expected, but feel free to fork.

---

*Happy Lunar New Year! 🧧*
