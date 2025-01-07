# Projet PPII - Semestre S5

## Table des matières
1. [Introduction](#introduction)
2. [Membres du groupe](#membres-du-groupe)
3. [Description du projet](#description-du-projet)
4. [Prérequis](#prérequis)
5. [Installation](#installation)
6. [Exécution](#exécution)

---

## Introduction

Bienvenue dans le projet **PPII - Semestre S5**. Ce projet est réalisé dans le cadre du semestre 5 pour l'unité PPII. Vous trouverez ici toutes les informations nécessaires pour comprendre, installer, et exécuter le projet.


## Membres du groupe

- **Girres Elisa** - [elisa.girres@telecomnancy.eu](mailto:elisa.girres@telecomnancy.eu)
- **Briand Thibault** - [thibault.briand@telecomnancy.eu](mailto:thibault.briand@telecomnancy.eu)
- **Denys Angèle** - [angele.denys@telecomnancy.eu](mailto:angele.denys@telecomnancy.eu)
- **Regennass Anne** - [anne.regennass@telecomnancy.eu](mailto:anne.regennass@telecomnancy.eu)


## Description du projet

- **Sujet :** Développement d'une application web pour un jeu de société avec intelligence artificielle
- **Objectifs :** Recréer le jeu de société dit du "Blokus" avec toutes ses règles et spécificités, jouable de 1 à 4 joueurs avec participation possible d'IA performantes.
- **Technologies utilisées :** Algorithme de Monte-Carlo, Algorithme du min-max, HTML, JavaScript, CSS, SocketIO, Python 


## Prérequis

Prérequis nécessaires pour utiliser ce projet :

- **Langage(s) :** Python 3.10, HTML, JavaScript, CSS, SQLite3
- **Frameworks :** Flask 3.1.0, Flask-SocketIO 5.5.0, Django
- **Dépendances :** Voir le fichier `requirements.txt`


## Installation

Comment installer le projet sur une machine locale:

### Étapes générales :

1. Clonez ce dépôt :
   ```bash
   git clone https://gibson.telecomnancy.univ-lorraine.fr/projets/2425/ppii-s5/grp6
   cd grp6
   ```

2. Créez un environnement python:
    ```bash
    python3 -m venv venv
    ```

3. Lancez cet environnement: 
(NB: après exécution, vérifiez la présence de l'intituté "(venv)" en amont du chemin du répertoire dans lequel vous vous trouvez)
    ```bash
    source venv/bin/activate
    ```

4. Installez les dépendances:
    ```bash
    pip install -r requirements.txt
    ```


## Exécution

Avant exécution, soyez informé que cette implémentation nécessite un minimum de performances de la part de votre machine. Ainsi, un processus un minima performant est vivement conseillé pour la meilleure expérience de jeu possible. 
Autrement, le jeu tournera tout de même, seulement le temps de calcul de l'IA sera plus lente, malgré l'optimisation effectuée sur celle-ci.


1. Verifiez que l'environnement python est bien lancé. Sinon, écrivez l'instruction suivante: 
(En supposant le processus d'installation effectué)
    ```bash
    source venv/bin/activate
    ```

2. Lancer l'application :

    ```bash
    python code_pages.py
    ```

3. Naviguer dans la page web selon les désirs.

