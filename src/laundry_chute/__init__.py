from .downloader import DriveDownloader
from .fetcher import SheetParser
from .bridge import AdbBridge
import os

__all__ = ["DriveDownloader", "SheetParser"]

def main(): 
    downloader = DriveDownloader(".config/key.json")
    root_id = "1NiZ9rL19qKLqt0uNcP5tIqc0fUrksAPs"
    fetcher = SheetParser()
    fetcher.connect(".config/key.json")
    charts = fetcher.fetch_charts(
        "https://docs.google.com/spreadsheets/d/1cA5Wpi5n8_0O79tUqjNabMA3WWyzJYJ2kV6yN7Ig0Xo/edit?usp=sharing", 
        "Phase 3: Road to 15k"
    )
    
    for chart in charts:
        id = downloader.get_folder_id(
            root_id, 
            chart.version, 
            chart.name, 
            chart.type
        )
        downloader.download_folder(id, f"downloads/{chart.name}")
        
    # file_to_move = zip_all_subfolders("downloads")
    # print(file_to_move)
    # return
    
    bridge = AdbBridge("/sdcard/Android/data/com.Reflektone.AstroDX/files/levels/")
    bridge.connect()
    for folder in os.listdir("downloads"):
        bridge.push_package(f"downloads/{folder}")
