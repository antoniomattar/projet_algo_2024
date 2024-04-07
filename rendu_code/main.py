#!/usr/bin/env python3
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
from tools.tycat import read_instance
from tools.ray_casting import point_in_polygon
from tools.aire_polygone import aire_shoelace

def trouve_inclusions(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    n = len(polygones)
    liste_inclusions = [-1 for i in range(n)]
    #ALGORITHME QUI MELANGE AIRE_DECROISSANTE ET BOUDING QUADRANT
    from tools.in_quadrant import point_in_quadrant
    # PREMIEREMENT, ON TRIE DANS L'ORDRE DÉCROISSANT LES POLYGONES PAR AIRE
    liste_tuple_aire_polygones = [(polygones[i].bounding_quadrant(),aire_shoelace(polygones[i]),i) for i in range(n)]
    liste_tuple_aire_polygones.sort(key=lambda tup:tup[1],reverse = True)
    n -= 1
    while liste_tuple_aire_polygones:
        # RECUPERATION DU DERNIER POLYGONE : ON LE SUPPRIME
        polygone = liste_tuple_aire_polygones.pop()
        n -= 1
        # ON SE RAMENE AU PREMIER POINT DU POLYGONE
        indice_polygone = polygone[2]
        aire_polygone = polygone[1]
        premier_point = polygones[indice_polygone].points[0]
        # ET ON VERIFIE S'IL EST INCLUT DANS UN POLYGONE PLUS GRAND
        for i in range(n, -1, -1):
            quadrant = liste_tuple_aire_polygones[i][0]
            id = liste_tuple_aire_polygones[i][2]
            if aire_polygone < liste_tuple_aire_polygones[i][1]:
                if point_in_quadrant(premier_point,quadrant):
                    if point_in_polygon(premier_point,polygones[id]):
                        liste_inclusions[indice_polygone] = id
                        break
    return liste_inclusions

def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = trouve_inclusions(polygones)
        print(inclusions)


if __name__ == "__main__":
    main()
