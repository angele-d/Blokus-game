import sys
import os

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fonc_DB import *
def test_tour():
    with app.app_context():
        result = tour(135)[1]
        expected_result = 'R'
        assert result == expected_result