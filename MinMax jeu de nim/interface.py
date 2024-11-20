from time import sleep
import nim as jeu

import humain1 as joueur1
import minmax as joueur2 #Joueur2 peut être humain2 ou aleatoire ou minmax

def change_joueur(joueur_courant):
    '''
    Changer la valeur de joueur_courant ("joueur1" ou "joueur2")
    :param joueur_courant: (string)
    '''
    if joueur_courant == joueur1:
        joueur_courant = joueur2
        print("C'est au tour du joueur 2:")
    else:
        joueur_courant = joueur1
        print("C'est au tour du joueur 1:")
    return joueur_courant
    pass


#CrÃ©er la variable situation et lui affecter la situation initiale
situation = jeu.situation_initiale()
#affecter 'joueur2' Ã  la variable joueur_courant
joueur_courant = joueur2
#afficher la rÃ¨gle du jeu (avec la bonne fonction du module nim)
jeu.regle()
#afficher la situation (avec la bonne fonction du module nim)
print("")
print("Affichage des alumettes en jeu:")
jeu.affiche(situation)
#tant que le jeu n'est pas terminÃ© :
while jeu.est_fini(situation) == False:
    print("--------------------------")
    #changer le joueur courant
    joueur_courant = change_joueur(joueur_courant)
    #faire jouer le joueur courant et affecter son coup dans la variable coup
    sleep(1)
    coup = joueur_courant.joue(situation)
    #mettre Ã  jour la situation en tenant compte du coup jouÃ©
    situation = jeu.maj_situation(situation,coup)
    #afficher la nouvelle situation
    jeu.affiche(situation)

if joueur_courant == joueur1:
    print("-------- Résultats --------")
    print("Joueur1 a perdu")
else:
    print("-------- Résultats --------")
    print("Joueur2 a perdu") 