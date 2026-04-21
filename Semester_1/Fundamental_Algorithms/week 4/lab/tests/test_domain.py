import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from domain import create_concert
from utils import *

def test_create_concert():
    concert = create_concert("Muse", "Berlin", "05/09/2026", 150.0)
    assert get_artist(concert) == "Muse"
    assert get_city(concert) == "Berlin"
    assert get_date(concert) == "05/09/2026"
    assert get_price(concert) == 150.0

test_create_concert()