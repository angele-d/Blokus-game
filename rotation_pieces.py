from pieces import P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21 #pieces.py

def transformation(piece, isflipped,rotation):
    '''Le fait de retourner une pièce est de la tournée ne commute pas
    il faut donc ce décider sur une convention qui est appliquée par cette fonction
    ainsi, merci de n'utiliser que cette dernière pour que tout soit compatible'''
    if isflipped :
        m= flip(piece)
        m = rotation_piece_5x5(m,rotation)
        return m
    else: 
        return rotation_piece_5x5

def rotationx1(piece):
    '''
    Effectue 1 rotation d'une piece
    :param piece: matrice 5x5 de la piece originale
    :return: matrice 5x5 du resultat de la rotation
    SENS ANTIHORAIRE
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
    SENS ANTIHORAIRE
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
    result = [[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    for i in range(5):
        for j in range(5):
            if piece[i][j] != -1:
                result[i][4-j] = piece[i][j]
    return result
