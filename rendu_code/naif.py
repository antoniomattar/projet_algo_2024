#!/usr/bin/env python3
"""
Module pour les algorithmes naïfs de détection d'inclusions
- naif : algorithme naïf de détection d'inclusions
- naif_dyn : algorithme naïf de détection d'inclusions avec stockage des aires
- naif_quadrant : algorithme naïf de détection d'inclusions avec vérification de quadrant
"""
import tools.ray_casting as ray_casting
from tools.aire_polygone import aire_shoelace

def trouve_inclusions(polygones,mode="naif_quadrant"):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    liste_inclusions = [-1 for i in range(len(polygones))]
    def definit_aire_min(id_polygone):
        """
        Fonction utilisée plusieurs fois afin de définir dans le dictionnaire
        définit dans les différents algorithmes
        pour stocker le plus petit parent d'un polygone
        """
        if dico_inclusions[id_polygone] != []:
            # OBTENTION DU POLYGONE D'AIRE MINIMALE PARMI LES PERES
            id_aire_min = dico_inclusions[id_polygone][0]
            aire_min = aire_shoelace(polygones[id_aire_min])
            for id_autre_polygone in dico_inclusions[id_polygone][1:]:
                aire_actuelle = aire_shoelace(polygones[id_autre_polygone])
                if aire_actuelle < aire_min:
                    id_aire_min = id_autre_polygone
                    aire_min = aire_actuelle
            liste_inclusions[id_polygone] = id_aire_min

    # ALGORITHME NAÏF
    if mode == "naif":
        n = len(polygones)
        # IDÉE : PRENDRE UN POINT DE CHAQUE POLYGONE
        # TESTER S'IL Y A UN POLYGONE DANS LEQUEL IL EST
        # INCLUS

        # TABLE DE HACHAGE QUI VA CONTENIR TOUS LES PARENTS D'UN POLYGONE
        dico_inclusions = {}
        # POUR UN POLYGONE i DONNE...
        for i in range(n):
            polygone = polygones[i]
            # ... ON AJOUTE LE POLYGONE i A LA TABLE DE HACHAGE...
            dico_inclusions[i] = []
            # ... ON SE RAMENE AU PREMIER POINT DU POLYGONE i...
            premier_point = polygone.points[0]
            # ... ET ON VERIFIE SI CE POINT EST DANS UN AUTRE POLYGONE
            for j in range(n):
                if i != j:
                    if ray_casting.point_in_polygon(premier_point,polygones[j]):
                        dico_inclusions[i].append(j)
        # MAINTENANT QUE L'ON A TOUS LES PARENTS, ON TROUVE LE PLUS PETIT
        for id_polygone in dico_inclusions:
            definit_aire_min(id_polygone)

    # ALGORITHME NAÏF AVEC STOCKAGE DES AIRES
    elif mode == "naif_dyn":
        n = len(polygones)
        # IDÉE : MÊME CHOSE MAIS ON GARDE EN MEMOIRE LES AIRES
        # TABLE DE HACHAGE QUI VA CONTENIR TOUS LES PARENTS D'UN POLYGONE
        dico_inclusions = {}
        # DICTIONNAIRE QUI VA STOCKER LES AIRES POUR NE PAS RECALCULER PLUSIEURS FOIS
        dico_aire = {}
        # POUR UN POLYGONE i DONNE...
        for i in range(n):
            polygone = polygones[i]
            # ... ON AJOUTE SON AIRE DANS LE DICTIONNAIRE ...
            dico_aire[i] = aire_shoelace(polygone)
            # ... ON AJOUTE LE POLYGONE i A LA TABLE DE HACHAGE...
            dico_inclusions[i] = []
            # ... ON SE RAMENE AU PREMIER POINT DU POLYGONE i...
            premier_point = polygone.points[0]
            # ... ET ON VERIFIE SI CE POINT EST DANS UN AUTRE POLYGONE
            for j in range(n):
                if i != j:
                    if ray_casting.point_in_polygon(premier_point, polygones[j]):
                        dico_inclusions[i].append(j)
        # MAINTENANT QUE L'ON A TOUS LES PARENTS, ON TROUVE LE PLUS PETIT
        for id_polygone in dico_inclusions:
           definit_aire_min(id_polygone)

    elif mode == "naif_quadrant":
        from tools.in_quadrant import point_in_quadrant
        n = len(polygones)
        # IDÉE : LA MÊME CHOSE
        # MAIS ON REGARDE D'ABORD SI ON EST
        # DANS LE QUADRANT DU POLYGONE AVANT DE TESTER L'INCLUSION

        # TABLE DE HACHAGE QUI VA CONTENIR TOUS LES PARENTS D'UN POLYGONE
        dico_inclusions = {}
        polygones_quadrant = [polygone.bounding_quadrant() for polygone in polygones]
        # POUR UN POLYGONE i DONNE...
        for i in range(n):
            polygone = polygones[i]
            # ... ON AJOUTE LE POLYGONE i A LA TABLE DE HACHAGE...
            dico_inclusions[i] = []
            # ... ON SE RAMENE AU PREMIER POINT DU POLYGONE i...
            premier_point = polygone.points[0]
            # ... ET ON VERIFIE SI CE POINT EST DANS UN AUTRE POLYGONE
            for j in range(n):
                if i != j:
                    if point_in_quadrant(premier_point, polygones_quadrant[j]):
                        if ray_casting.point_in_polygon(premier_point, polygones[j]):
                            dico_inclusions[i].append(j)
        # MAINTENANT QUE L'ON A TOUS LES PARENTS, ON TROUVE LE PLUS PETIT
        for id_polygone in dico_inclusions:
            definit_aire_min(id_polygone)
    
    else: raise ValueError("mode non reconnu")

    return liste_inclusions
