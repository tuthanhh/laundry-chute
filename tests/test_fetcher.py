from laundry_chute.fetcher import SheetParser


def test_client_connect():
    fetcher = SheetParser()
    fetcher.connect(".config/key.json")
    assert fetcher.client is not None


def test_fetch_charts():
    fetcher = SheetParser()
    fetcher.connect(".config/key.json")
    charts = fetcher.fetch_charts(
        "https://docs.google.com/spreadsheets/d/1cA5Wpi5n8_0O79tUqjNabMA3WWyzJYJ2kV6yN7Ig0Xo/edit?usp=sharing", 
        "Phase 3: Road to 15k"
    )
    assert len(charts) != 0
    print(charts)
