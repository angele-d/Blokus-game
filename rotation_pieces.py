from pieces import P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21 #pieces.py

def rotationx1(piece):
    '''
    Effectue 1 rotation d'une piece
    :param piece: matrice 5x5 de la piece originale
    :return: matrice 5x5 du resultat de la rotation
    '''
    temp = [[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    k = -1
    for j in range(4,-1,-1):
        k += 1
        for i in range(5):
            temp[k][i] = piece[i][j]
    return temp

def rotation_piece_5x5(piece,rotation):
    '''
    Effectue <rotation> rotations d'une pièce
    :param piece: matrice 5x5 de la piece originale
    :param rotation: (int)
    :return: matrice 5x5 du resultat des rotations
    '''
    rotate = rotation%4
    result = piece
    while rotate > 0:
        result = rotationx1(result)
        rotate = rotate - 1
    return result

def flip(piece):
    '''
    Retourne la piece par symetrie selon la verticale (colonne 2)
    :param piece: matrice 5x5 de la piece originale
    :return: matrice 5x5 du resultat du retournement de pièce
    '''
    if piece in [P1,P2,P3,P5,P7,P8,P10,P14,P17,P18,P20]:
        return piece
    else:
        result = [[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
        for i in range(5):
            for j in range(5):
                if piece[i][j] != -1:
                    result[i][4-j] = piece[i][j]
        return result
