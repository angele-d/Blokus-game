matrice_exemple = [['V'] * 20] *20

def print_jeu(m):
    for i in m:
        for j in i:
            print('[',j,']',end='')
        print('\n') 


def matrice_possible(m,p):
    for i in m:
        for j in i:
            if m[i][j] == p:
                if m[i+1][j+1] == 'V':
                    m[i+1][j+1] = 'P'
                if m[i-1][j+1] == 'V':
                    m[i-1][j+1] = 'P'
                if m[i+1][j-1] == 'V':
                    m[i+1][j-1] = 'P'
                if m[i-1][j-1] == 'V':
                    m[i-1][j-1] = 'P'
    for i in m:
        for j in i:
            if m[i][j] == p:
                if m[i+1][j] == 'V' or 'P':
                    m[i+1][j] = 'I'
                if m[i-1][j] == 'V' or 'P':
                    m[i-1][j] = 'I'
                if m[i][j+1] == 'V' or 'P':
                    m[i][j+1] = 'I'
                if m[i][j-1] == 'V' or 'P':
                    m[i][j-1] = 'I'
    return m
                



def coup_possible(m,p,x,y,rot,flip):
    