import json
from collections import deque

class Defis_2:
    def __init__(self, fichier_defis) -> None:

        with open(fichier_defis, 'r') as f:
            self.defis = json.load(f)

    def couleur(self):
        """
        Vérifie si les couleurs dans les défis sont valides en comparant avec des listes de couleurs en français et en anglais.
        :return: la clef du dictionnaire colors correspondant à la même couleur que sa clef, sinon False
        """
        # Création d'un dictionnaire inversé pour les couleurs en français
        dict = {"silver": "argent",
                "beige": "beige",
                "white": "blanc",
                "blue": "bleu",
                "coral": "corail",
                "indigo": "indigo",
                "yellow": "jaune",
                "lavender": "lavande",
                "magenta": "magenta",
                "brown": "marron",
                "mauve": "mauve",
                "black": "noir",
                "olive": "olive",
                "gold": "or",
                "orange": "orange",
                "orchid": "orchidée",
                "pink": "rose",
                "red": "rouge",
                "salmon": "saumon",
                "green": "vert"}

        for cle, valeur in self.defis["colors"].items():
            for c, v in dict.items():
                if cle == valeur:
                    return cle
                elif (cle == c) and (valeur == v):
                    return cle
                elif (cle == v) and (valeur == c):
                    return cle
        return False

    def reflexion(self):
        """
        Recherche la position de la lampe "L" dans la map.
        :param map: Liste de listes représentant la map.
        :return: Tuple (ligne, colonne) représentant la position de la lampe, sinon False.
        """
        ligne_lampe = None
        colonne_lampe = None
        for i, ligne in enumerate(self.defis["map"]):
            if "L" in ligne:
                ligne_lampe = i
                colonne_lampe = ligne.index("L")
                if i == 0:
                    direction_lampe = "bas"
                elif i == len(self.defis["map"])-1:
                    direction_lampe = "haut"
                elif colonne_lampe == 0:
                    direction_lampe = "droite"
                elif colonne_lampe == len(ligne)-1:
                    direction_lampe = "gauche"
                
                return self.deplacement_lumiere(ligne_lampe, colonne_lampe, direction_lampe)
        return False
            
    def verifier_obstacle(self, ligne, colonne, direction):
        """
        Vérifie si la case à la position (ligne, colonne) de la map contient un obstacle "/" ou "\\" et
        renvoie la nouvelle direction en fonction de l'obstacle.
        :param ligne: Entier représentant la ligne.
        :param colonne: Entier représentant la colonne.
        :param direction: String représentant la direction ("haut", "bas", "gauche", "droite").
        :return: String représentant la nouvelle direction.
        """
        obstacle = self.defis["map"][ligne][colonne]
        correspondances = {("/","haut"): "droite", ("/","bas"): "gauche", ("/","droite"): "haut", ("/","gauche"): "bas",
                        ("\\","haut"): "gauche", ("\\","bas"): "droite", ("\\","droite"): "bas", ("\\","gauche"): "haut"}
        return correspondances.get((obstacle, direction), direction)
    
    def deplacement_lumiere(self, ligne, colonne, direction):
        """
        Recherche la position de la lampe "L" dans la map et déplace la lumière en suivant les règles du jeu.
        :param ligne: Entier représentant la ligne de départ de la lumière.
        :param colonne: Entier représentant la colonne de départ de la lumière.
        :param direction: String représentant la direction initiale de la lumière ("haut", "bas", "gauche", "droite").
        :return: Entier représentant la valeur de la case atteinte par la lumière.
        """
        while True:
            # Vérifier si la case actuelle est un entier
            if isinstance(self.defis["map"][ligne][colonne], int):
                return self.defis["map"][ligne][colonne]
            else:
                # Appeler la fonction vérifier_obstacle pour obtenir la direction à suivre
                direction = self.verifier_obstacle(ligne, colonne, direction)

                # Mettre à jour les coordonnées en fonction de la direction
                if direction == "bas":
                    ligne += 1
                elif direction == "haut":
                    ligne -= 1
                elif direction == "droite":
                    colonne += 1
                elif direction == "gauche":
                    colonne -= 1

    def calcul(self):
        """
        Trouve les ensembles de nombres dans la liste 'numbers' qui s'additionnent pour obtenir le résultat 'result'.
        Returns:
            list: Une liste de listes contenant les ensembles de nombres qui s'additionnent pour obtenir le résultat cible.
        """
        result = self.defis["result"]
        numbers = self.defis["numbers"]
        res = []
        numbers.sort()  # Trie les nombres pour obtenir les combinaisons dans l'ordre croissant
        self.trouver_combinaisons_recursif(0, result, [], numbers, res)  # Appel initial de la fonction auxiliaire avec un total cible de 'result'
        
        output = []
        for solution in res:
            solution.sort()
            output.append('+'.join([str(x) for x in solution]))
        
        return output

    def trouver_combinaisons_recursif(self, start, target, path, numbers, res):
        """
        Fonction auxiliaire pour effectuer un parcours récursif avec retour en arrière.
        
        Args:
            start (int): L'indice de départ pour le parcours.
            target (int): La somme cible à atteindre.
            path (list): La liste des nombres sélectionnés jusqu'à présent.
            numbers (list): La liste de nombres.
            res (list): La liste des résultats.
        """
        if target == 0:
            # Si la somme cible est atteinte, ajouter la liste de nombres dans les résultats
            res.append(path[:])
        elif target < 0:
            # Si la somme cible est dépassée, revenir en arrière
            return
        else:
            for i in range(start, len(numbers)):
                # Parcourir la liste de nombres à partir de l'indice 'start'
                if i > start and numbers[i] == numbers[i-1]:
                    # Ignorer les doublons pour éviter de répéter les nombres dans la combinaison
                    continue
                if numbers[i] not in path:
                    # Ignorer les nombres qui sont déjà dans la combinaison
                    path.append(numbers[i])
                    self.trouver_combinaisons_recursif(i + 1, target - numbers[i], path, numbers, res)  # Appel récursif avec le nouveau total cible
                    path.pop()  # Retour en arrière (trouver_combinaisons_recursif)

    def frequence(self):
        """
        :return: Le mot le moins représenté (str)
        """
        word_count = {}
        for ligne in self.defis["words"]:
            for word in ligne:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
            
        return min(word_count, key=word_count.get)

    def manquant(self):
        """
        Fonction permettant de trouver le premier nombre manquant dans une liste de nombres.
        :return: int: Le premier nombre manquant dans la liste de nombres.
        """
        list_color = []  # Utilisation d'un ensemble pour stocker les couleurs disponibles
        list_numbers_color1 = []  # Utilisation d'un ensemble pour stocker les nombres de couleur 1
        list_numbers_color2 = []  # Utilisation d'un ensemble pour stocker les nombres de couleur 2

        # Permet de récupérer les couleurs disponibles et de les mettre dans "list_color"
        for color in self.defis["numbers"]:
            list_color.append(color[-1])  # Ajouter la dernière lettre de chaque couleur à l'ensemble list_color

        # Permet de récupérer les nombres et de les mettre dans leur ensemble respectif
        for color in self.defis["numbers"]:
            if color[-1] == list(list_color)[0]:  # Comparer la dernière lettre de la couleur avec la première lettre de list_color (converti en liste)
                list_numbers_color1.append(int(color[:-1]))  # Ajouter le nombre à l'ensemble list_numbers_color1 (en convertissant la chaîne de caractères en entier)
            else:
                list_numbers_color2.append(int(color[:-1]))  # Ajouter le nombre à l'ensemble list_numbers_color2 (en convertissant la chaîne de caractères en entier)

        list_numbers_color1.sort()
        list_numbers_color2.sort()

        # Trouver le premier nombre manquant dans list_numbers_color1
        for number in range(len(list_numbers_color1)-1):
            if list_numbers_color1[number+1] != list_numbers_color1[number]+1:
                return list_numbers_color1[number]+1

        # Trouver le premier nombre manquant dans list_numbers_color2
        for number in range(len(list_numbers_color2)-1):
            if list_numbers_color2[number+1] != list_numbers_color2[number]+1:
                return list_numbers_color2[number]+1

        return False  # Retourner False si tous les nombres sont présents

    def labyrinthe(self):
        """
        Cherche les coordonnées de la case départ
        :return: la fonction "parcours_labyrinthe"
        """
        ligne_start = None
        colonne_start = None

        # Recherche de la position de départ en utilisant des indices
        for i in range(len(self.defis["map"])):
            if "D" in self.defis["map"][i]:
                ligne_start = i
                colonne_start = self.defis["map"][i].index("D")
                break  # Sortir de la boucle dès que la position de départ est trouvée

        return self.parcours_labyrinthe(ligne_start, colonne_start, derniere_direction="")

    def parcours_labyrinthe(self, ligne, colonne, derniere_direction):
        """
        Fonction permettant de parcourir un labyrinthe en utilisant une approche BFS.

        Args:
            ligne (int): Numéro de la ligne actuelle.
            colonne (int): Numéro de la colonne actuelle.
            derniere_direction (str): Dernière direction prise ("haut", "bas", "gauche", "droite").

        Returns:
            int: 1 si la case est marquée comme "1"
            int: 2 si la case est marquée comme "2"
            int: 3 si la case est marquée comme "3"
            int: 4 si la case est marquée comme "4"
        """
        queue = deque([(ligne, colonne, derniere_direction)])
        arrivees = ["1", "2", "3", "4"]

        while queue:
            ligne, colonne, derniere_direction = queue.popleft()
            case = self.defis["map"][ligne][colonne]

            if case == "1":
                return 1
            elif case == "2":
                return 2
            elif case == "3":
                return 3
            elif case == "4":
                return 4

            max_ligne = len(self.defis["map"])
            max_colonne = len(self.defis["map"][0])

            # Mouvement vers le haut
            if (ligne > 0) and (self.defis["map"][ligne-1][colonne] == "" or self.defis["map"][ligne-1][colonne] in arrivees) and ((derniere_direction != "haut") or (derniere_direction == "")):
                queue.append((ligne-1, colonne, "bas"))

            # Mouvement vers le bas
            if (ligne < max_ligne-1) and (self.defis["map"][ligne+1][colonne] == "" or self.defis["map"][ligne+1][colonne] in arrivees) and ((derniere_direction != "bas") or (derniere_direction == "")):
                queue.append((ligne+1, colonne, "haut"))

            # Mouvement vers la gauche
            if (colonne > 0) and (self.defis["map"][ligne][colonne-1] == "" or self.defis["map"][ligne][colonne-1] in arrivees) and ((derniere_direction != "gauche") or (derniere_direction == "")):
                queue.append((ligne, colonne-1, "droite"))

            # Mouvement vers la droite
            if (colonne < max_colonne-1) and (self.defis["map"][ligne][colonne+1] == "" or self.defis["map"][ligne][colonne+1] in arrivees) and ((derniere_direction != "droite") or (derniere_direction == "")):
                queue.append((ligne, colonne+1, "gauche"))

    def doublon(self):
        """
        Recherche un mot en double dans la liste de mots fournie.
        :return: (str) Le mot en double s'il existe, sinon un message indiquant qu'il n'y a pas de mot en double.
        """
        word_count = {}
        for ligne in self.defis["words"]:
            for word in ligne:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

        # Retourne le mot en double
        for cle, valeur in word_count.items():
            if valeur == 2:
                return cle
            
        return "Il n'y a pas de mot en double"

    def raisonnement(self):
        """
        Applique un raisonnement sur le dessin en utilisant différentes méthodes pour vérifier s'il y a une solution possible.
        :return: Le nom de la solution trouvée, sinon (str) "Aucune de ces solutions n'est la bonne".
        """
        drawing = self.defis["drawing"]
        pieces = self.defis["pieces"]

        # On regarde si il y a possibilité d'enlever des colonnes à droite du dessin
        decalage = self.decalage_raisonnement(drawing)

        # On décale chaque ligne du dessin par "decalage"
        new_drawing = [ligne[decalage:] for ligne in drawing if "" in ligne]

        # On regarde si il y a possibilité d'enlever des colonnes à gauche du dessin mais pour cela on va inverser chaque ligne du dessin
        new_drawing = self.retourne_raisonnement(new_drawing)
        # On regarde si il y a possibilité d'enlever des colonnes à droite du dessin
        decalage_new_drawing = self.decalage_raisonnement(new_drawing)

        # On décale chaque ligne du dessin par "decalage_new_drawing"
        finish_drawing = [ligne[decalage_new_drawing:] for ligne in new_drawing if "" in ligne]

        # On remet le dessin à l'endroit
        finish_drawing = self.retourne_raisonnement(finish_drawing)
        # On inverse le vide ("") avec les murs ("X")
        finish_drawing = self.inversion_raisonnement(finish_drawing)
        # On regarde si une solution est possible
        for nom, map in pieces.items():
            if finish_drawing == map:
                return nom

        return "Aucune de ces solutions n'est la bonne"

    def decalage_raisonnement(self, drawing):
        """
        Recherche le décalage possible le plus à gauche du dessin en vérifiant chaque ligne.
        :param drawing: (list) Le dessin représenté sous forme de liste de listes.
        :return: (int) Le décalage possible le plus à gauche du dessin.
        """
        possibilite_decalage = []
        arrete_for = False
        # On parcourt chaque ligne de "drawing"
        for ligne in drawing:
            decalage = 0
            compteur = 0 # Pour savoir si on est au début de la ligne
            # On parcourt chaque symbole surla ligne
            for symbole in ligne:
                # Si le symbole est un trou et qu'il se trouve au début de la ligne
                if (symbole == "") and (compteur == 0):
                    decalage = 0
                    return decalage
                elif symbole == "X":
                    decalage += 1
                # Sinon on arrête les boucles "for"
                else:
                    possibilite_decalage.append(decalage)
                    break
                
                compteur += 1

            if arrete_for:
                break

        return min(possibilite_decalage)

    def retourne_raisonnement(self, drawing):
        """
        Retourne horizontalement chaque ligne du dessin.
        :param drawing: (list) Le dessin représenté sous forme de liste de listes.
        :return: (list) Le dessin modifié avec chaque ligne retournée horizontalement.
        """
        new_drawing = []
        for ligne in drawing:
            new_drawing.append(ligne[::-1])

        return new_drawing

    def inversion_raisonnement(self, drawing):
        """
        Inverse les cases vides ("") avec les cases pleines ("X") dans le dessin.
        :param drawing: (list) Le dessin représenté sous forme de liste de listes.
        :return: (list) Le dessin modifié avec les cases inversées.
        """
        for ligne in range(len(drawing)):
            for colonne in range(len(drawing[ligne])):
                if drawing[ligne][colonne] == "":
                    drawing[ligne][colonne] = "X"
                else:
                    drawing[ligne][colonne] = ""
        return drawing

    def main(self):
        if self.defis["type"] == "couleur":
            print(self.couleur())
        elif self.defis["type"] == "reflexion":
            print(self.reflection())
        elif self.defis["type"] == "calcul":
            print(self.calcul())
        elif self.defis["type"] == "frequence":
            print(self.frequence())
        elif self.defis["type"] == "manquant":
            print(self.manquant())
        elif self.defis["type"] == "labyrinthe":
            print(self.labyrinthe())
        elif self.defis["type"] == "doublon":
            print(self.doublon())
        elif self.defis["type"] == "raisonnement":
            print(self.raisonnement())




if __name__ == "__main__":
    read_json_couleur = "C:/Users/aubru/Documents/Professionnel/MI/P5/Projets/Cortex Challenge/cortex-challenge-test/cards/card-1.json"
    read_json_reflection = "C:/Users/aubru/Documents/Professionnel/MI/P5/Projets/Cortex Challenge/cortex-challenge-test/cards/card-2.json"
    read_json_calcul = "C:/Users/aubru/Documents/Professionnel/MI/P5/Projets/Cortex Challenge/cortex-challenge-test/cards/card-3.json"
    read_json_frequence = "C:/Users/aubru/Documents/Professionnel/MI/P5/Projets/Cortex Challenge/cortex-challenge-test/cards/card-4.json"
    read_json_manquant = "C:/Users/aubru/Documents/Professionnel/MI/P5/Projets/Cortex Challenge/cortex-challenge-test/cards/card-5.json"
    read_json_labyrinthe = "C:/Users/aubru/Documents/Professionnel/MI/P5/Projets/Cortex Challenge/cortex-challenge-test/cards/card-6.json"
    read_json_doublon = "C:/Users/aubru/Documents/Professionnel/MI/P5/Projets/Cortex Challenge/cortex-challenge-test/cards/card-7.json"
    read_json_raisonnement = "C:/Users/aubru/Documents/Professionnel/MI/P5/Projets/Cortex Challenge/cortex-challenge-test/cards/card-8.json"

    Cortex_challenge = Defis_2(read_json_couleur)
    Cortex_challenge.main()
    Cortex_challenge = Defis_2(read_json_reflection)
    Cortex_challenge.main()
    Cortex_challenge = Defis_2(read_json_calcul)
    Cortex_challenge.main()
    Cortex_challenge = Defis_2(read_json_frequence)
    Cortex_challenge.main()
    Cortex_challenge = Defis_2(read_json_manquant)
    Cortex_challenge.main()
    Cortex_challenge = Defis_2(read_json_labyrinthe)
    Cortex_challenge.main()
    Cortex_challenge = Defis_2(read_json_doublon)
    Cortex_challenge.main()
    Cortex_challenge = Defis_2(read_json_raisonnement)
    Cortex_challenge.main()