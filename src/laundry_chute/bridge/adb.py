import shutil
import subprocess
import time

from .base import Bridge

MAX_RETRIES = 3


class AdbBridge(Bridge):
    def connect(self) -> bool:
        if not shutil.which("adb"):
            print("❌ Critical Error: 'adb' is not installed or not in PATH.")
            print("   -> Please install Android Platform Tools.")
            return False

        try:
            result = subprocess.run(
                ["adb", "devices"], text=True, capture_output=True, check=True
            )
            lines = result.stdout.strip().split("\n")
            devices = [line for line in lines if "\tdevice" in line]

            if not devices:
                print("⚠️ No device found. Is USB Debugging enabled?")
                return False

            print(f"✅ Connected to: {devices[0].split()[0]}")
            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ ADB Error: {e}")
            return False

    def push_package(self, package_path: str) -> bool:
        for attempt in range(MAX_RETRIES):
            try:
                subprocess.run(
                    ["adb", "push", package_path, self.device_destination], check=True
                )
                print(f"✅ Package pushed to {self.device_destination}")
                return True
            except subprocess.CalledProcessError as e:
                if attempt < MAX_RETRIES - 1:
                    print(
                        f"⚠️ Push failed (attempt {attempt + 1}/{MAX_RETRIES}), retrying..."
                    )
                    time.sleep(2)
                else:
                    print(f"❌ Push failed after {MAX_RETRIES} attempts: {e}")
                    return False
