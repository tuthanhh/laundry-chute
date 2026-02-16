from laundry_chute import DriveDownloader, SheetParser
def test_get_id(): 
    downloader = DriveDownloader(".config/key.json")
    root_id = "1NiZ9rL19qKLqt0uNcP5tIqc0fUrksAPs"
    id = downloader.get_folder_id(
        root_id, 
        "UNiVERSE PLUS", 
        "Estahv", 
        "DX"
    )
    print(id)
    assert id is not None
    
def test_download_simple():
    downloader = DriveDownloader(".config/key.json")
    root_id = "1NiZ9rL19qKLqt0uNcP5tIqc0fUrksAPs"
    id = downloader.get_folder_id(
        root_id, 
        "UNiVERSE PLUS", 
        "Estahv", 
        "DX"
    )
    print(id)
    assert id is not None
    
    downloader.download_folder(id, "downloads")

def test_fetch_and_download():
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
        
    assert True
