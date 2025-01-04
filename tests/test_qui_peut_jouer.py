import sys
import os

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fonc_DB import *
def test_qui_peut_jouer():
    result = qui_peut_jouer(1,128)
    expected_result = ['B']
    assert result == expected_result