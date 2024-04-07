#!/usr/bin/env python3
"""Module pour la detection de point dans un polygone avec l'algorithme de ray casting"""
import geo.point
import geo.polygon

def point_in_polygon(point : geo.point.Point, polygon: geo.polygon.Polygon, epsilon=0.0000001):
    """Renvoie True si le point est dans le polygone, False sinon 
    (algorithme de ray casting) avec epsilon precision"""
    n = len(polygon.points)
    x, y = point.coordinates
    inside = False
    p1x, p1y = polygon.points[0].coordinates
    for i in range(n+1):
        p2x, p2y = polygon.points[i % n].coordinates
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters + epsilon:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside