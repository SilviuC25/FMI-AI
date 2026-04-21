import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from domain import *
from services import *

def test_add_concert_to_list():
    concerts = []
    concert = create_concert("Muse", "Berlin", "05/09/2026", 150.0)
    add_concert_to_list(concerts, concert)
    assert len(concerts) == 1

def test_modify_concert():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 185.0)]
    modify_concert(concerts, 0, new_price=200.0)
    assert get_price(concerts[0]) == 200.0

def test_calculate_average_price():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 180.0), 
                create_concert("Coldplay", "London", "15/08/2026", 360.0)]
    artist = "Coldplay"
    average_price = calculate_average_price(artist, concerts)
    assert average_price == 270.0

def test_remove_concerts_by_artist():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 180.0), 
                create_concert("Muse", "London", "20/08/2026", 200.0)]
    updated_concerts = remove_concerts_by_artist(concerts, "Coldplay")
    assert len(updated_concerts) == 1
    assert get_artist(updated_concerts[0]) == "Muse"

def test_remove_concerts_by_price_interval():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 180.0), 
                create_concert("Muse", "London", "20/08/2026", 200.0),
                create_concert("U2", "Dublin", "10/09/2026", 300.0)]
    updated_concerts = remove_concerts_by_price_interval(concerts, 150.0, 250.0)
    assert len(updated_concerts) == 1
    assert get_artist(updated_concerts[0]) == "U2"

def test_remove_concerts_by_time_interval():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 180.0), 
                create_concert("Muse", "London", "20/08/2026", 200.0),
                create_concert("U2", "Dublin", "10/09/2026", 300.0)]
    updated_concerts = remove_concerts_by_time_interval(concerts, "01/08/2026", "31/08/2026")
    assert len(updated_concerts) == 2
    artists = [get_artist(concert) for concert in updated_concerts]
    assert "Coldplay" in artists
    assert "U2" in artists

def test_display_concerts_by_city():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 180.0), 
                create_concert("Muse", "London", "20/08/2026", 200.0),
                create_concert("U2", "Paris", "10/09/2026", 300.0)]
    paris_concerts = display_concerts_by_city(concerts, "Paris")
    assert len(paris_concerts) == 2
    for concert in paris_concerts:
        assert get_city(concert) == "Paris"

def test_display_concerts_by_city_andartist():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 180.0), 
                create_concert("Muse", "London", "20/08/2026", 200.0),
                create_concert("Coldplay", "Paris", "10/09/2026", 300.0)]
    coldplay_paris_concerts = display_concerts_by_city_andartist(concerts, "Paris", "Coldplay")
    assert len(coldplay_paris_concerts) == 2
    for concert in coldplay_paris_concerts:
        assert get_city(concert) == "Paris"
        assert get_artist(concert) == "Coldplay"

def test_display_concerts_below_price():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 180.0), 
                create_concert("Muse", "London", "20/08/2026", 200.0),
                create_concert("U2", "Dublin", "10/09/2026", 300.0)]
    cheap_concerts = display_concerts_below_price(concerts, 250.0)
    assert len(cheap_concerts) == 2
    for concert in cheap_concerts:
        assert get_price(concert) < 250.0

def test_filter_concerts_by_artists_and_price():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 180.0), 
                create_concert("Muse", "London", "20/08/2026", 200.0),
                create_concert("U2", "Dublin", "10/09/2026", 300.0)]
    filtered_concerts = filter_concerts_by_artists_and_price(concerts, ["Coldplay", "U2"], 250.0)
    assert len(filtered_concerts) == 1
    assert get_artist(filtered_concerts[0]) == "Coldplay"

def test_filter_concerts_by_price_and_date():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 180.0), 
                create_concert("Muse", "London", "20/08/2026", 200.0),
                create_concert("U2", "Dublin", "10/09/2026", 300.0)]
    filtered_concerts = filter_concerts_by_price_and_date(concerts, 250.0, "31/08/2026")
    assert len(filtered_concerts) == 2
    artists = [get_artist(concert) for concert in filtered_concerts]
    assert "Coldplay" in artists
    assert "Muse" in artists

def test_undo_last_operation():
    concerts = []
    concert1 = create_concert("Coldplay", "Paris", "15/07/2026", 180.0)
    add_concert_to_list(concerts, concert1)
    concerts_history = []
    concerts_history.apppend(concert1[:])
    concert2 = create_concert("Muse", "London", "20/08/2026", 200.0)
    add_concert_to_list(concerts, concert2)
    concerts_history.append(concerts[:])
    concerts = undo_last_operation(concerts_history)
    assert len(concerts) == 1
    assert get_artist(concerts[0]) == "Coldplay"
    assert len(concerts_history) == 1


def run_tests():
    test_add_concert_to_list()
    test_modify_concert()
    test_calculate_average_price()
    test_remove_concerts_by_artist()
    test_remove_concerts_by_price_interval()
    test_remove_concerts_by_time_interval()
    test_display_concerts_by_city()
    test_display_concerts_by_city_andartist()
    test_display_concerts_below_price()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()