import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from domain import create_concert
from services import add_concert_to_list, modify_concert, calculate_average_price

def test_add_concert_to_list():
    concerts = []
    concert = create_concert("Muse", "Berlin", "05/09/2026", 150.0)
    add_concert_to_list(concerts, concert)
    assert len(concerts) == 1

def test_modify_concert():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 185.0)]
    modify_concert(concerts, 0, new_price=200.0)
    assert concerts[0]["price"] == 200.0

def test_calculate_average_price():
    concerts = [create_concert("Coldplay", "Paris", "15/07/2026", 180.0), 
                create_concert("Coldplay", "London", "15/08/2026", 360.0)]
    artist = "Coldplay"
    average_price = calculate_average_price(artist, concerts)
    assert average_price == 270.0

test_add_concert_to_list()
test_modify_concert()
test_calculate_average_price()