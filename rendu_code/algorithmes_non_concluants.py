#!/usr/bin/env python3
"""
Module pour les algorithmes non concluants de détection d'inclusions
"""
import tools.ray_casting as ray_casting

def trouve_inclusions(polygones,mode="grid"):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    liste_inclusions = [-1 for i in range(len(polygones))]
    
    # ALGORITHME DE MAILLAGE
    if mode == "grid":
        # IDÉE : ON MAILLE LES POLYGONES EN FONCTION DE LEURS AIRES (UN MAILLAGE PAR POLYGONE)
        # ON STOCKE LES POINTS EN TANT QUE CLÉS DANS UN DICTIONNAIRE AVEC COMME
        # VALEURS LES INDICES DES POLYGONES DANS LESQUELS ILS SONT INCLUS
        # ON PARCOURT LES POINTS DES POLYGONES ET ON LES AJOUTE AU DICTIONNAIRE
        # SI ILS SONT DANS UN POLYGONE

        points_grid = {}

        def grid_points(x0, y0, step, n):
            """
            create a grid of points.
            """
            for i in range(n):
                for j in range(n):
                    yield Point([x0 + i * step, y0 + j * step])

        for i in range(len(polygones)):
            polygone = polygones[i]
            aire_polygone = ray_casting.aire_polygone(polygone)
            # ON CREE UN MAILLAGE POUR LE POLYGONE
            for point in polygone.points:
                x = point.coordinates[0]
                y = point.coordinates[1]
                # ON CHERCHE LES POINTS DANS LE MAILLAGE (grid_points a ecrire)
                step = int(aire_polygone / 100)
                n = int(aire_polygone / 10)
                for point_grid in grid_points(x, y, step, n):
                    if ray_casting.point_in_polygon(point_grid, polygone):
                        if point_grid not in points_grid:
                            points_grid[point_grid] = [i]
                        else:
                            points_grid[point_grid].append(i)

        # ON PARCOURT LES POINTS ET ON REGARDE DANS QUELS POLYGONES ILS SONT
        for point in points_grid:
            if len(points_grid[point]) > 1:
                for i in range(len(points_grid[point])):
                    for j in range(i+1, len(points_grid[point])):
                        if ray_casting.point_in_polygon(point, polygones[points_grid[point][i]]):
                            liste_inclusions[points_grid[point][i]] = points_grid[point][j]
                        else:
                            liste_inclusions[points_grid[point][j]] = points_grid[point][i]

    # ALGORITHME TRIANGULATION
    elif mode == "triangulation":
        import numpy as np
        from geo.point import Point
        from geo.polygon import Polygon
        from scipy.spatial import Delaunay
        n = len(polygones)
        # TABLE DE HACHAGE QUI VA CONTENIR TOUS LES PARENTS D'UN POLYGONE
        dico_inclusions = {}
        dico_aire = {}

        def convertit_polygone_en_liste_triangle(polygone):
            liste = []
            for point in polygone.points:
                liste.append(point.coordinates)
            points = np.array(liste)
            tri = Delaunay(points)
            liste_triangle = points[tri.simplices]
            liste_triangle = liste_triangle.tolist()
            for j in range(len(liste_triangle)):
                for i in range(3):
                    liste_triangle[j][i] = Point(liste_triangle[j][i])
                liste_triangle[j] = Polygon(liste_triangle[j])
            return liste_triangle
        liste_triangles = []
        for i in range(n):
            for triangle in convertit_polygone_en_liste_triangle(polygones[i]):
                liste_triangles.append([triangle, i])
        liste_aire = [ray_casting.aire_polygone(
            polygones[i]) for i in range(n)]

        for i in range(n):
            polygone = polygones[i]
            dico_aire[i] = ray_casting.aire_polygone(polygone)
            premier_point = polygone.points[0]
            dico_inclusions[i] = []
            for j in range(len(liste_triangles)):
                if ray_casting.point_in_polygon(premier_point,liste_triangles[j][0]):
                   if i!= liste_triangles[j][1]:
                    dico_inclusions[i].append(liste_triangles[j][1])
                    break
        # MAINTENANT QUE L'ON A TOUS LES PARENTS, ON TROUVE LE PLUS PETIT
        for id_polygone in dico_inclusions:
            if dico_inclusions[id_polygone] != []:
                # OBTENTION DU POLYGONE D'AIRE MINIMALE PARMI LES PERES
                id_aire_min = dico_inclusions[id_polygone][0]
                aire_min = dico_aire[id_aire_min]
                for id_autre_polygone in dico_inclusions[id_polygone][1:]:
                    aire_actuelle = dico_aire[id_autre_polygone]
                    if aire_actuelle < aire_min:
                        id_aire_min = id_autre_polygone
                        aire_min = aire_actuelle
                liste_inclusions[id_polygone] = id_aire_min

    # ALGORITHME MEMOIRE DES HAUTEURS
    elif mode == "hauteur_sauvegarde":
        n = len(polygones)
        liste_premiers_points = [polygone.points[0] for polygone in polygones]
        liste_hauteur = [point.coordinates[1] for point in liste_premiers_points]
        dico_hauteur_abs = {y : [] for y in liste_hauteur}

        def calcul_limite(polygone):
            max_x,max_y = 0, 0
            for point in polygone.points:
                x,y = point.coordinates
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            return max_x, max_y

        def ajoute_dico_abcisse(point,indice):
            polygone = polygones[indice]
            x, y = point.coordinates
            p1, p2 = polygone.points[-1], polygone.points[0]
            p1x,p1y = p1.coordinates
            p2x,p2y = p2.coordinates
            i = 0
            while (p1, p2) != (polygone.points[-2], polygone.points[-1]):
                if p2y != p1y:
                    calcul_x = ((y - p1y)*(p2x - p1x))/(p2y - p1y) + p1x
                    dico_hauteur_abs[y].append((calcul_x,i))
                p1, p2 = polygone.points[i], polygone.points[i + 1]
                i += 1
            print("j'arrête le while x)")

        def ajoute_indice_avec_x_juste_avant(y,x,indice):
            liste = dico_hauteur_abs[y]
            if liste != []:
                print(liste)
                max = (liste[0][0],-1)
                for i in range(len(liste)):
                    if max[0] <= liste[i][0] < x:
                        max = liste[i]
                liste_inclusions[indice] = max[1]
            liste_inclusions[indice] = -1


        for i in range(n):
            polygone = polygones[i]
            max_x,max_y = calcul_limite(polygone)
            for premier_point in liste_premiers_points:
                x,y = premier_point.coordinates
                if x < max_x and y < max_y:
                    ajoute_dico_abcisse(premier_point,i)
            
        print(dico_hauteur_abs)
        
        for i in range(n):
            x, y = premier_point.coordinates
            ajoute_indice_avec_x_juste_avant(y,x,i)

    else: raise ValueError("mode non reconnu")
    
    return liste_inclusions
