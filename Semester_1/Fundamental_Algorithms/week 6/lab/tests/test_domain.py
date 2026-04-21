import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from domain import *
from utils import *

def test_create_concert():
    concert = create_concert("Muse", "Berlin", "05/09/2026", 150.0)
    assert get_artist(concert) == "Muse"
    assert get_city(concert) == "Berlin"
    assert get_date(concert) == "05/09/2026"
    assert get_price(concert) == 150.0

def test_get_concerts_in_date_interval():
    concerts = [
        create_concert("Artist1", "CityA", "10/09/2026", 100.0),
        create_concert("Artist2", "CityB", "12/09/2026", 120.0),
        create_concert("Artist3", "CityC", "15/09/2026", 130.0),
    ]
    filtered_concerts = get_concerts_in_date_interval(concerts, "11/09/2026", "13/09/2026")
    assert len(filtered_concerts) == 1
    assert get_artist(filtered_concerts[0]) == "Artist2"

def test_sort_concerts_by_price():
    concerts = [
        create_concert("Artist1", "CityA", "10/09/2026", 150.0),
        create_concert("Artist2", "CityB", "12/09/2026", 100.0),
        create_concert("Artist3", "CityC", "15/09/2026", 200.0),
    ]
    sorted_concerts = sort_concerts_by_price(concerts)
    assert get_price(sorted_concerts[0]) == 100.0
    assert get_price(sorted_concerts[1]) == 150.0
    assert get_price(sorted_concerts[2]) == 200.0

def run_tests():
    test_create_concert()
    test_get_concerts_in_date_interval()
    test_sort_concerts_by_price()
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()

