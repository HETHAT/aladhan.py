import aladhan


def test_current():
    with aladhan.Client() as client:
        assert isinstance(client.get_current_time("Africa/Algiers"), str)
        assert isinstance(client.get_current_date("Africa/Algiers"), str)
        assert isinstance(client.get_current_timestamp("Africa/Algiers"), int)
        assert isinstance(client.get_current_islamic_year(), int)
        assert isinstance(client.get_current_islamic_month(), int)
