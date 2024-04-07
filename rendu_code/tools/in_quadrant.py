#!/usr/bin/env python3
"""Savoir si un point est dans un carré"""
import geo.point
import geo.polygon
import geo.quadrant


def point_in_quadrant(point : geo.point.Point,quadrant : geo.quadrant.Quadrant):
    coord_min_x, coord_min_y = quadrant.min_coordinates
    coord_max_x, coord_max_y = quadrant.max_coordinates
    x,y = point.coordinates
    return (coord_min_x < x < coord_max_x and coord_min_y < y < coord_max_y)

