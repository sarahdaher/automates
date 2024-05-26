def trouver_maximum_local(tableau):
    gauche = 0
    droite = len(tableau) - 1

    while gauche <= droite:
        milieu = (gauche + droite) // 2

        # Vérifie si le milieu est un maximum local
        if (milieu == 0 or tableau[milieu] >= tableau[milieu - 1]) and \
           (milieu == len(tableau) - 1 or tableau[milieu] >= tableau[milieu + 1]):
            return milieu

        # Si le maximum local est à gauche du milieu
        if milieu > 0 and tableau[milieu - 1] > tableau[milieu]:
            droite = milieu - 1
        # Si le maximum local est à droite du milieu
        else:
            gauche = milieu + 1

    return -1

# Exemple d'utilisation
tableau = [1, 3, 4, 0, 1, 3, 8, 9, 14]
indice_max_local = trouver_maximum_local(tableau)
print("Indice d'un maximum local:", indice_max_local)
