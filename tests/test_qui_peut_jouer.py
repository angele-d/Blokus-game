import sys
import os

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fonc_DB import *
def test_qui_peut_jouer():
    result = qui_peut_jouer(2,111)
    expected_result = ['B','Y']
    assert result == expected_result