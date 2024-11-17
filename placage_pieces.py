from pieces import P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21 #pieces.py
from rotation_pieces import transformation


#Manque les informations sur comment est faite la BD

def placer_piece_grille20x20(grille,num_piece,x,y,couleur,rotation,isflipped):
    pi = transformation(num_piece,isflipped,rotation)
    for i in range(len(pi)):
        for j in range(len(pi)):
            if pi[i][j]:
                grille[x+i-2][y+j-2] = couleur
    return grille


def transcription_pieces_SQL_grille():
    pass

