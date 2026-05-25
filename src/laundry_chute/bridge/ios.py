import atexit
import os
import shutil
import subprocess

from .base import Bridge


class IosBridge(Bridge):
    def __init__(self, mount_point: str, bundle_id: str):
        super().__init__(mount_point)
        self.bundle_id = bundle_id

    def connect(self) -> bool:
        if not shutil.which("ifuse"):
            print("❌ Critical Error: 'ifuse' is not installed or not in PATH.")
            return False

        os.makedirs(self.device_destination, exist_ok=True)

        try:
            subprocess.run(
                [
                    "ifuse",
                    "--documents",
                    self.bundle_id,
                    self.device_destination,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ iOS Error: {e}")
            return False

        atexit.register(self._unmount)
        print(f"✅ Mounted at {self.device_destination}")
        return True

    def _unmount(self):
        subprocess.run(
            ["fusermount", "-u", self.device_destination], stderr=subprocess.DEVNULL
        )

    def push_package(self, package_path: str) -> bool:
        levels_dir = os.path.join(self.device_destination, "levels")
        os.makedirs(levels_dir, exist_ok=True)

        dest = os.path.join(levels_dir, os.path.basename(package_path))
        try:
            for root, _, files in os.walk(package_path):
                rel = os.path.relpath(root, package_path)
                target_dir = dest if rel == "." else os.path.join(dest, rel)
                os.makedirs(target_dir, exist_ok=True)
                for f in files:
                    shutil.copyfile(os.path.join(root, f), os.path.join(target_dir, f))
            print(f"✅ Package copied to {dest}")
            return True
        except OSError as e:
            print(f"❌ iOS Error: {e}")
            return False
