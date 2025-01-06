import sys
import os

# Ajouter le répertoire parent au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logique_jeu import *
def test_coup_rajoute_no_parral():
    m=[['B','B','V','V','B','V','V','V','V','V','V','V','V','V','V','V','V','V','R','R'],
    ['B','B','V','V','V','B','V','V','V','V','V','V','V','V','V','V','V','V','R','V'],
    ['V','V','B','B','B','V','B','V','V','V','V','V','V','V','V','V','V','V','R','V'],
    ['B','B','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V'],
    ['B','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V'],
    ['V','B','B','B','B','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V'],
    ['B','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V'],
    ['B','B','B','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V'],
    ['V','V','V','B','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V'],
    ['V','V','B','B','B','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V'],
    ['V','B','V','V','V','V','V','V','V','V','V','V','B','B','V','V','V','V','V','V'],
    ['B','B','V','V','V','V','V','V','V','V','V','B','B','V','B','V','V','V','V','V'],
    ['B','V','V','V','V','V','V','V','V','V','V','B','V','V','B','V','V','V','V','V'],
    ['V','B','B','B','B','B','V','V','V','V','B','V','V','V','B','B','B','V','V','V'],
    ['B','V','V','V','V','V','V','V','B','B','B','V','V','V','V','V','V','V','V','V'],
    ['B','B','B','B','V','V','V','V','B','V','V','V','V','V','V','V','V','V','V','V'],
    ['V','V','V','V','B','B','V','V','V','B','B','B','V','V','V','V','V','V','V','V'],
    ['V','V','B','B','B','V','B','B','V','B','V','B','V','V','V','V','V','V','V','V'],
    ['G','G','V','V','V','V','B','B','B','V','V','V','V','V','V','V','V','V','V','V'],
    ['G','G','V','V','V','V','V','V','V','V','V','V','V','V','V','V','V','Y','Y','Y']]
    result = coup_rajoute_no_parral(m,[(1,3),(5,1),(5,3)],['P18','P19','P20','P21'],'B')
    expected_result = [('P18', 'B', 7, 5, 2, False), ('P19', 'B', 7, 5, 1, False), ('P19', 'B', 7, 5, 2, False),
                       ('P20', 'B', 7, 5, 1, False), ('P20', 'B', 7, 5, 2, False), ('P20', 'B', 7, 5, 3, False),
                       ('P20', 'B', 7, 5, 4, False), ('P21', 'B', 7, 5, 4, False), ('P18', 'B', 7, 5, 4, True),
                       ('P19', 'B', 7, 5, 1, True), ('P19', 'B', 7, 5, 4, True), ('P20', 'B', 7, 5, 1, True),
                       ('P20', 'B', 7, 5, 2, True), ('P20', 'B', 7, 5, 3, True),
                       ('P20', 'B', 7, 5, 4, True), ('P21', 'B', 7, 5, 2, True)]
    result = [i for i in result if i not in expected_result]
    assert result == []