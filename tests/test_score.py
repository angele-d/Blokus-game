import sys
import os

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from score import *
def test_score():
    result = score(50)
    expected_result = [-91, -86]
    assert result == expected_result