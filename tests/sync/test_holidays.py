import aladhan


def test_holidays():
    with aladhan.Client() as client:
        assert client.get_hijri_holidays(10, 12) == ["Eid-ul-Adha", "Hajj"]
        assert isinstance(client.get_next_hijri_holiday(), aladhan.Date)
        _ = client.get_islamic_holidays(1442)
        assert isinstance(_, list), isinstance(_[0], aladhan.Date)
