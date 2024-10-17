# PROJET 4 DE LA FORMATION PYTHON : TOURNOI D'ECHEC

## Clonage du repo github

Placez vous dans le dossier où vous souhaitez importer le projet et ouvrez la console, tapez :

`git clone https://github.com/ThibaultGERARDIN/pythonProjet4.git`


## Création de l'environnement virtuel (venv)

Une fois dans le dossier cloné, vous devez initialiser l'environnement virtuel

### Directement depuis la console :

Sur macOS/Linux :\
`python3 -m venv .venv`
> Vous devrez peut-être run `sudo apt-get install python3-venv` d'abord sur un OS Debian

Sur Windows :\
`python -m venv .venv`
> Vous pouvez aussi utiliser la commande `py -3 -m venv .venv`

### Depuis VsCode :

Ouvrez la palette de commande (Ctrl+Shift+P) et cherchez `Python: Create Environment` puis selectionnez l'option Venv, et choisissez la dernière version de Python pour l'interprete.

## Initialisation du programme

Une fois le dossier cloné et venv créé, il vous faut installer les dépendances nécessaires (uniquement tabulate pour l'affichage des données sous forme de tableaux) : `pip install -r requirements.txt` ou `pip install tabulate`

## Utilisation du programme

Pour tester le fonctionnement vous pouvez utiliser la liste "test_players.json" en la renommant "players.json". Il y a également un tournoi "test20241016-172141.json" dans la liste des tournois passés pour tester l'affichage des anciens tournoi.

Lancez le programme `main.py` et naviguez les menus à votre guise ! 