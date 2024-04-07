#!/usr/bin/env python3
"""
Module pour la detection d'inclusions de polygones en utilisant l'aire des polygones
"""
import tools.ray_casting as ray_casting
from tools.aire_polygone import aire_shoelace


def trouve_inclusions(polygones,mode="aire_decroissante"):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    liste_inclusions = [-1 for i in range(len(polygones))]

    # ALGORITHME : TRI DES AIRES DE MANIERE DECROISSANTE
    if mode == "aire_decroissante":
        n = len(polygones)
        # PREMIEREMENT, ON TRIE DANS L'ORDRE DÉCROISSANT LES POLYGONES PAR AIRE
        liste_tuple_aire_polygones = [(polygones[i], aire_shoelace(polygones[i]), i) for i in range(n)]
        liste_tuple_aire_polygones.sort(key=lambda tup: tup[1], reverse=True)
        n -= 1
        while liste_tuple_aire_polygones:
            # RECUPERATION DU DERNIER POLYGONE : ON LE SUPPRIME
            polygone = liste_tuple_aire_polygones.pop()
            n -= 1
            # ON SE RAMENE AU PREMIER POINT DU POLYGONE
            indice_polygone = polygone[2]
            aire_polygone = polygone[1]
            premier_point = polygone[0].points[0]
            # ET ON VERIFIE S'IL EST INCLUT DANS UN POLYGONE PLUS GRAND
            for i in range(n, -1, -1):
                if aire_polygone < liste_tuple_aire_polygones[i][1]:
                    if ray_casting.point_in_polygon(premier_point, liste_tuple_aire_polygones[i][0]):
                        liste_inclusions[indice_polygone] = liste_tuple_aire_polygones[i][2]
                        break

    # ALGORITHME : COMPARAISON D'AIRES AU MOMENT DES CALCULS
    elif mode == "aire_decroissante_dico":
        n = len(polygones)
        # IDEE : CREER UN DICTIONNAIRE QUI ENREGISTRE POUR UN POLYGONE i
        # L'AIRE DE i, ET L'AIRE DE SON PERE ACTUEL
        dico_eligible = {}
        for i in range(n):
            # ON CALCUL L'AIRE DE TOUS LES POLYGONES i ...
            aire_i = aire_shoelace(polygones[i])
            # ... QUE L'ON STOCKE DANS LE DICTIONNAIRE...
            dico_eligible[i] = [aire_i]
            for j in range(i):
                # ON STOCKE L'AIRE DES POLYGONES j DEJA PRESENTS DANS LE DICTIONNAIRE...
                aire_j = dico_eligible[j][0]
                # ... SI j PEUT ETRE INCLUS DANS i
                if aire_j < aire_i:
                    premier_point_j = polygones[j].points[0]
                    # SOIT j N'A PAS DE PÈRE...
                    if len(dico_eligible[j]) == 1:
                        # ALORS S'IL EST DANS i, CELUI-CI DEVIENT SON PÈRE
                        if ray_casting.point_in_polygon(premier_point_j, polygones[i]):
                            dico_eligible[j].append(aire_i)
                            liste_inclusions[j] = i
                    # SINON j A UN PÈRE ...
                    else:
                        # SI i EST PLUS PETIT QUE LE PÈRE ACTUEL ...
                        if aire_i < dico_eligible[j][1]:
                            # ON VERIFIE SI j EST BIEN DANS i
                            if ray_casting.point_in_polygon(premier_point_j, polygones[i]):
                                dico_eligible[j][1] = aire_i
                                liste_inclusions[j] = i
                # SINON i PEUT ETRE INCLUS DANS j
                elif aire_j > aire_i:
                    premier_point_i = polygones[i].points[0]
                    # SOIT i N'A PAS DE PÈRE...
                    if len(dico_eligible[i]) == 1:
                        # ALORS S'IL EST DANS j, CELUI-CI DEVIENT SON PÈRE
                        if ray_casting.point_in_polygon(premier_point_i, polygones[j]):
                            dico_eligible[i].append(aire_j)
                            liste_inclusions[i] = j
                    # SINON i A UN PÈRE ...
                    else:
                        # SI j EST PLUS PETIT QUE LE PÈRE ACTUEL ...
                        if aire_j < dico_eligible[i][1]:
                            # ON VÉRIFIE SI i EST BIEN DANS j
                            if ray_casting.point_in_polygon(premier_point_i, polygones[j]):
                                dico_eligible[i][1] = aire_j
                                liste_inclusions[i] = j

    # ALGORITHME AIRE "MERGE"
    elif mode == "aire_decroissante_merge":
        n = len(polygones)
        # IDÉE : FAIRE UN MERGE DES AIRES IDENTIQUES AFIN DE NE BALAYER QUE
        # LES AIRES STRICTEMENT SUPÉRIEURES
        liste_tuple_aire_polygones = [(polygones[i], aire_shoelace(polygones[i]), i) for i in range(n)]
        liste_tuple_aire_polygones.sort(key=lambda tup: tup[1], reverse=True)

        def merge_meme_valeur(liste):
            """
            Pour une liste triée de 3-tuples (décroissante pour la deuxième valeur),
            fusionne les valeurs similaires, la liste devient une liste où le premier élément
            est une aire, le deuxième est une liste de couples qui contiennent polygones[i] et i
            """
            if liste == []:
                return liste
            i = 1
            valeur_prec = liste[0]
            new_liste = [[valeur_prec[1], [(valeur_prec[0], valeur_prec[2])]]]
            l = []
            while i < len(liste):
                valeur_prec = liste[i-1]
                valeur_actuelle = liste[i]
                if valeur_actuelle[1] == valeur_prec[1]:
                    new_liste[0][1].append(
                        (valeur_actuelle[0], valeur_actuelle[2]))
                else:
                    l.append(new_liste[0])
                    new_liste = [[valeur_actuelle[1], [
                        (valeur_actuelle[0], valeur_actuelle[2])]]]
                i = i+1
            l.append(new_liste[0])
            return l
        liste_tuple_aire_polygones = merge_meme_valeur(liste_tuple_aire_polygones)
        n = len(liste_tuple_aire_polygones) - 1
        while liste_tuple_aire_polygones:
            # RECUPERATION DU DERNIER POLYGONE : ON LE SUPPRIME
            polygone = liste_tuple_aire_polygones.pop()
            n -= 1
            # ON SE RAMENE AU PREMIER POINT DU POLYGONE

            for couple in polygone[1]:
                indice_polygone = couple[1]
                aire_polygone = polygone[0]
                premier_point = couple[0].points[0]
                # ET ON VERIFIE S'IL EST INCLUT DANS UN POLYGONE PLUS GRAND
                for i in range(n, -1, -1):
                    for couple_2 in liste_tuple_aire_polygones[i][1]:
                        est_dedans = ray_casting.point_in_polygon(
                            premier_point, couple_2[0])
                        if est_dedans:
                            liste_inclusions[indice_polygone] = couple_2[1]
                            break
                    if est_dedans:
                        break

    # ALGORITHME UTILISANT DES ARBRES
    elif mode == "aire_croissante_arbre":
        from tools.in_quadrant import point_in_quadrant
        from tools.arbre_polygone import Arbre
        # IDÉE : ON MET DANS DANS UN ARBRE LES POLYGONES,
        # SI i EST LE FILS DE j, ALORS j EST LE PLUS PETIT
        # POLYGONE DANS LEQUEL i EST INCLUS
        n = len(polygones)
        # PREMIEREMENT, ON TRIE DANS L'ORDRE DÉCROISSANT LES POLYGONES PAR AIRE
        polygones_quadrant = [polygone.bounding_quadrant()
                                for polygone in polygones]
        liste_tuple_aire_polygones = [
            (aire_polygone(polygones[i]), i) for i in range(n)]
        liste_tuple_aire_polygones.sort(key=lambda tup: tup[0])
        arbre_poly = Arbre()

        def ajoute_polygone(arbre, indice):
            """
            Permet de mettre à jour la liste des inclusions
            tout en ajoutant les polygones à l'arbre
            progressivement
            """
            retour = False
            for feuille in arbre.feuille:
                if point_in_quadrant(polygones[indice].points[0], polygones_quadrant[feuille.racine]):
                    if ray_casting.point_in_polygon(polygones[indice].points[0], polygones[feuille.racine]):
                        ajoute_polygone(feuille, indice)
                        retour = True
                        break
            if retour == False:
                liste_inclusions[indice] = arbre.racine
                arbre.feuille.append(Arbre(indice))
        while liste_tuple_aire_polygones:
            _, indice = liste_tuple_aire_polygones.pop()
            ajoute_polygone(arbre_poly,indice)
    
    #ALGORITHME QUI MELANGE AIRE_DECROISSANTE ET BOUDING QUADRANT
    elif mode == "aire_decroissante_quadrant":
        from tools.in_quadrant import point_in_quadrant
        n = len(polygones)
        # PREMIEREMENT, ON TRIE DANS L'ORDRE DÉCROISSANT LES POLYGONES PAR AIRE
        liste_tuple_aire_polygones = [(polygones[i],aire_shoelace(polygones[i]),i) for i in range(n)]
        liste_tuple_aire_polygones.sort(key=lambda tup:tup[1],reverse = True)
        polygones_quadrant = [polygone[0].bounding_quadrant() for polygone in liste_tuple_aire_polygones]
        n -= 1
        while liste_tuple_aire_polygones:
            # RECUPERATION DU DERNIER POLYGONE : ON LE SUPPRIME
            polygone = liste_tuple_aire_polygones.pop()
            n -= 1
            # ON SE RAMENE AU PREMIER POINT DU POLYGONE
            indice_polygone = polygone[2]
            aire_polygone = polygone[1]
            premier_point = polygone[0].points[0]
            # ET ON VERIFIE S'IL EST INCLUT DANS UN POLYGONE PLUS GRAND
            for i in range(n, -1, -1):
                if aire_polygone < liste_tuple_aire_polygones[i][1]:
                    if point_in_quadrant(premier_point,polygones_quadrant[i]):
                        if ray_casting.point_in_polygon(premier_point,liste_tuple_aire_polygones[i][0]):
                            liste_inclusions[indice_polygone] = liste_tuple_aire_polygones[i][2]
                            break

    else: raise ValueError("Mode non reconnu")


    return liste_inclusions
