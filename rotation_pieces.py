
def rotationx1(piece):
    temp = [[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]
    k = -1
    for j in range(4,-1,-1):
        k += 1
        for i in range(5):
            temp[k][i] = piece[i][j]
    return temp

def rotation_piece_5x5(piece,rotation):
    '''
    :param piece: matrice 5x5 de la piece originale
    :param rotation: (int)
    :return: matrice 5x5 du resultat de la rotation
    '''
    rotate = rotation%4
    result = piece
    while rotate > 0:
        result = rotationx1(result)
        rotate = rotate - 1
    return result

