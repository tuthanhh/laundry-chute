import subprocess
import shutil
import sys

class AdbBridge: 
    def __init__(self, device_destination: str):
        """
        Args:
            device_destination: Where to put the files on the phone.
            Standard AstroDX path is usually /sdcard/AstroDX/levels
        """
        self.device_destination = device_destination
        self._check_adb_installed()
    
    def _check_adb_installed(self):
        """Verifies that ADB is in the system PATH."""
        if not shutil.which("adb"):
            print("❌ Critical Error: 'adb' is not installed or not in PATH.")
            print("   -> Please install Android Platform Tools.")
            sys.exit(1)
    
    def connect(self): 
        try: 
            result = subprocess.run(["adb", "devices"], text=True, capture_output=True, check=True)
            lines = result.stdout.strip().split('\n')
                        
            # Filter out the header and empty lines
            devices = [line for line in lines if "\tdevice" in line]
            
            if not devices:
                print("⚠️ No device found. Is USB Debugging enabled?")
                return False
            
            print(f"✅ Connected to: {devices[0].split()[0]}")
            return True
            
        except Exception as e:
            print(f"❌ ADB Error: {e}")
            return False
    
    def push_package(self, package_path: str):
        try:
            subprocess.run(["adb", "push", package_path, self.device_destination], check=True)
            print(f"✅ Package pushed to {self.device_destination}")
            return True
        
        except Exception as e:
            print(f"❌ ADB Error: {e}")
            return False
