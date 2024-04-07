#!/usr/bin/env python3
"""Module pour le calcul de l'aire d'un polygone en utilisant la formule de Shoelace"""
import geo.polygon

"""Calcul de l'aire d'un polygone"""
def aire_shoelace(polygon : geo.polygon.Polygon):
    """Renvoie l'aire du polygone en utilisant la formule de Shoelace"""
    n = len(polygon.points)
    area = 0
    for i in range(n):
        area += polygon.points[i].coordinates[0] * polygon.points[(i+1) % n].coordinates[1]
        area -= polygon.points[i].coordinates[1] * polygon.points[(i+1) % n].coordinates[0]
    return abs(area) / 2
