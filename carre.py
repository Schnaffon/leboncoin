import argparse

def plus_grand_carre(x, y, plateau):
    """ Fonction de calcul du plus grand carré sur la droite d'un carreau [x, y]

    :param x:
    :param y:
    :return:
    """
    # UP
    okay = True
    cote = 0
    while(okay):
        for count in range(cote + 1):
            if plateau[x + cote][y + count] == False:
                okay = False
            if plateau[x + count][y + cote] == False:
                okay = False
        if okay:
            cote += 1
    temporary_x = x + cote - 1
    temporary_y = y

    okay = True
    while(okay):
        for count in range(cote + 1):
            if plateau[temporary_x - cote][temporary_y + count] == False:
                okay = False
            if plateau[temporary_x - count][temporary_y + cote] == False:
                okay = False
        if okay:
            cote += 1

    max_cote = cote
    base_x = temporary_x
    base_y = temporary_y


    #DOWN
    okay = True
    cote = 0
    while(okay):
        for count in range(cote + 1):
            if plateau[x - cote][y + count] == False:
                okay = False
            if plateau[x - count][y + cote] == False:
                okay = False
        if okay:
            cote += 1
    temporary_x = x - cote + 1
    temporary_y = y

    okay = True
    while(okay):
        for count in range(cote + 1):
            if plateau[temporary_x + cote][temporary_y + count] == False:
                okay = False
            if plateau[temporary_x + count][temporary_y + cote] == False:
                okay = False
        if okay:
            cote += 1
    temporary_x = temporary_x + cote - 1

    if cote > max_cote:
        max_cote = cote
        base_x = temporary_x
        base_y = temporary_y

    return (max_cote, base_x, base_y)

def parcours_plateau(plateau):
    """ On parcourt tout le plateau et on calcul le plus grand carré disponible sur la droite de chaque obstacle

    :return:
    """
    max_cote = 0
    base_x = 0
    base_y = 0

    for i in range(len(plateau)-1):
        for j in range(len(plateau[0])-1):
            if not plateau[i][j]:
                (cote, x, y) = plus_grand_carre(i, j+1, plateau)
                if cote > max_cote:
                    max_cote = cote
                    base_x = x
                    base_y = y

    for i in range(max_cote):
        for j in range(max_cote):
            plateau[base_x - i][base_y + j] = "plein" # Ici c'est un peu laid, le plateau devient hétérogène.


    for line in plateau[:-1]:
        for carreau in line[1:-1]:
            if carreau == "plein":
                print("x", end='')
            elif carreau:
                print(".", end='')
            else:
                print("o", end='')
        print("")

def load_plateau(file):
    """ Chargement du plateau sous forme d'une liste de listes de booléens

    :param file:
    :return:
    """
    plateau = []
    with open(file, 'r') as f:
        symbols = f.readline()
        plein = symbols[-2]
        obstacle = symbols[-3]
        vide = symbols[-4]
        taille = symbols[:-4]
        line = f.readline()
        while (line):
            content = [False] # ON ajoute un False au début de chaque ligne pour mieux gérer les bords
            for carreau in line:
                if carreau == ".":
                    content.append(True)
                elif carreau == "o":
                    content.append(False)
                elif carreau == "\n":
                    continue
                else:
                    raise ValueError
            content.append(False)
            plateau.append(content) # On ajoute un False à la fin de chaque ligne pour mieux gérer les bords
            line = f.readline()
        content = [False] * len(plateau[0]) # On ajoute une ligne de False pour représenter les bords plus simplement dans le calcul à venir
        plateau.append(content)
        return (plateau, taille, vide, obstacle, plein)

def verify_plateau(taille, plateau):
    """ Vérification de la cohérence en taille du plateau

    :param taille:
    :return:
    """
    print(plateau)
    largeur = len(plateau[0])
    if len(plateau) - 1 != int(taille):
        return False
    for line in plateau:
        if len(line) != largeur:
            return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('files', type=str, nargs='+',
                        help='an integer for the accumulator')
    args = parser.parse_args()
    for file in args.files:
        print(file)
        (plateau, taille, vide, obstacle, plein) = load_plateau(file)
        if not verify_plateau(taille, plateau):
            continue
        parcours_plateau(plateau)

def test_verification():
    plateau = [[True, True, False], [True, False]]
    assert not verify_plateau(2, plateau)
    plateau = [[True, True, False], [True,True, False]]
    assert not verify_plateau(3, plateau)
    assert verify_plateau(1, plateau)

def test_plus_grand_carre():
    plateau = [[False, True, True, False], [False, True, True, False], [False, False, False, False]]
    assert plus_grand_carre(1, 1, plateau) == (2, 1, 1)
