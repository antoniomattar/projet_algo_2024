#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from geo.tycat import tycat
from geo.polygon import Polygon
from geo.point import Point
from itertools import groupby


def print_polygons(polygons):
    print("we have", len(polygons), "polygons")
    tycat(*(poly.segments() for poly in polygons))


def read_instance(fname):
    with open(fname, 'rt') as f:
        points = (list(map(float, l.split())) for l in f)
        # create polygons from [(l, x, y)]
        return [
                Polygon([Point(p[1:]) for p in poly_points])
                for _, poly_points in groupby(points, key=lambda t: t[0])
        ]


def main():
    if len(sys.argv) <= 1:
        return

    for poly_file in sys.argv[1:]:
        print(poly_file)
        polys = read_instance(poly_file)
        print_polygons(polys)


if __name__ == "__main__":
    main()

