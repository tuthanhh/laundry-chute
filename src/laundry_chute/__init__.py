import argparse
import os
import sys
import tomllib

from .bridge import AdbBridge, IosBridge
from .downloader import DriveDownloader
from .fetcher import SheetParser

__all__ = ["DriveDownloader", "SheetParser"]


def main():
    parser = argparse.ArgumentParser(description="laundry-chute")
    parser.add_argument("--config", default=".config/settings.toml")
    parser.add_argument("--type", choices=["STD", "DX"])
    parser.add_argument("--os", choices=["android", "ios"], default="android")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--download-only", action="store_true")
    group.add_argument("--push-only", action="store_true")

    args = parser.parse_args()

    with open(args.config, "rb") as f:
        settings = tomllib.load(f)

    if not args.push_only:
        downloader = DriveDownloader(settings["key_file"], settings["root_id"])
        fetcher = SheetParser()
        fetcher.connect(settings["key_file"])
        charts = fetcher.fetch_charts(
            settings["sheet_url"],
            settings["worksheet"],
        )

        if args.type:
            charts = [c for c in charts if c.type.upper() == args.type.upper()]

        for chart in charts:
            folder_id = downloader.get_folder_id(chart.version, chart.name, chart.type)
            downloader.download_folder(folder_id, os.path.join(settings["download_dir"], chart.name))

    if not args.download_only:
        if args.os == "ios":
            bridge = IosBridge(settings["ios"]["mount_point"], settings["ios"]["id"])
        else:
            bridge = AdbBridge(settings["android"]["destination"])

        if not bridge.connect():
            print("Failed to perform file transfer")
            sys.exit(1)

        for folder in os.listdir(settings["download_dir"]):
            path = os.path.join(settings["download_dir"], folder)
            if not folder.startswith(".") and os.path.isdir(path):
                bridge.push_package(path)
