import sys
import os

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from placage_pieces import *
def test_piece_restante():
    result = piece_restante(97,'B')
    expected_result = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17,18,19,20,21]
    assert result == expected_result