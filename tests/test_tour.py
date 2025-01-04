import sys
import os

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fonc_DB import *
def test_tour():
    with app.app_context():
        result = tour(97)[1]
        expected_result = 'G'
        assert result == expected_result