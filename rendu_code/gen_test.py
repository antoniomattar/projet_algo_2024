#!/usr/bin/env python3
import random
from geo.point import Point
from geo.polygon import Polygon
import tools.tycat as tycat
import tools.ray_casting as ray_casting
from math import cos, sin
from math import pi as PI

# HANDMADE POLYGONS ######################################################################################
HANDMADE_POLYGONS = [
    Polygon([
        Point([18, 20]),
        Point([18, 16]),
        Point([14, 14]),
        Point([20, 12]),
        Point([22, 16]),
        Point([20, 16]),
        Point([20, 18]),
        Point([26, 20]),
        Point([22, 22])
    ]),

    Polygon([
        Point([30,0]),
        Point([34,6]),
        Point([40,6]),
    ]),


    Polygon([
        Point([20,-5]),
        Point([20,-15]),
        Point([35,-10]),
        Point([35, 0]),
        Point([45, -10]),
        Point([40, 15])
    ]),


    Polygon([
        Point([-25,6]),
        Point([-25,2]),
        Point([-22,1]),
        Point([-21,6]),
    ]),

    Polygon([
        Point([-24,12]),
        Point([-11,1]),
        Point([-20,-4]),
        Point([-23,-2]),
        Point([-30,-4]),
        Point([-29,7])
    ]),

    Polygon([
        Point([-35, 5]),
        Point([-34, -4]),
        Point([-41, 5]),
    ]),

    Polygon([
        Point([-12, 19]),
        Point([4,14]),
        Point([5, 5]),
        Point([-6, 7]),
        Point([-6, -17]),
        Point([-8, -7]),
        Point([-22, -6]),
        Point([-19, -15]),
        Point([-43, -2]),
        Point([-44, 9]),
        Point([-37, 8]),
        Point([-38, 21]),
        Point([-33, 21]),
        Point([-33, 9]),
        Point([-22, 19]),
        Point([-16, 7])
    ]),

    Polygon([
        Point([-40,85]),
        Point([-33,86]),
        Point([-32, 76]),
        Point([-27, 77]),
        Point([-25, 52]),
        Point([-40, 53])
    ]),

    Polygon([
        Point([-2,67]),
        Point([16, 68]),
        Point([15, 62]),
        Point([3, 63]),
        Point([-5, 39]),
        Point([-15, 45])
    ]),

    Polygon([
        Point([-40,105]),
        Point([-17,99]),
        Point([-17, 89]),
        Point([-23, 65]),
        Point([29, 77]),
        Point([22, 67]),
        Point([38, 66]),
        Point([37, 57]),
        Point([9,58]),
        Point([-5, 30]),
        Point([-27, 43]),
        Point([-61, 15]),
        Point([-48, 59]),
        Point([-68, 66]),
        Point([-46, 84])
    ])





]

############################################################################################################

# SQUARES ################################################################################################

def square(start_x, start_y, side):
    """
    create a square, horizontally aligned.
    used in test scripts as a quick way to get polygons.
    """
    starting_point = Point([start_x, start_y])
    points = [starting_point]
    points.append(Point([start_x + side, start_y]))
    points.append(Point([start_x + side, start_y + side]))
    points.append(Point([start_x, start_y + side]))
    return Polygon(points)

def nested_squares(x0: float, y0: float, side0: float, spacing: float, depth: int):
    """
    create a nested square pattern, with the biggest square at the top left corner.
    """
    polygons = []
    side = side0
    x = x0
    y = y0
    for _ in range(depth):
        polygons.append(square(x, y, side))
        x += spacing
        y += spacing
        side -= 2 * spacing
    return polygons

def aligned_squares(x0: float, y0: float, side: float, shift_x: float, shift_y: float, number: int):
    """
    create a pattern of squares, horizontally and vertically aligned.
    """
    assert max(shift_x, shift_y) > side
    x,y,s = x0,y0,side
    for _ in range(number):
        yield square(x,y,s)
        x += shift_x
        y += shift_y

def aligned_nested_squares(
        x0: float,
        y0: float,
        side0: float,
        spacing: float,
        depth: int,
        number: int
        ):
    """
    create a pattern of nested square patterns.
    """
    polygons = []
    x = x0
    y = y0
    for _ in range(number):
        polygons.extend(nested_squares(x, y, side0, spacing, depth))
        x += 2 * depth * spacing
    return polygons

def multiple_aligned_nested_squares(
        x0: float,
        y0: float,
        side0: float,
        spacing: float,
        depth: int,
        number_x: int ,
        number_y: int
    ):
    """
    create a pattern of aligned nested square patterns.
    """
    assert number_x > 0 and number_y > 0 and depth > 0 , "number_x, number_y and depth must be positive integers"
    assert depth >= spacing , "depth must be greater than or equal to spacing"
    polygons = []
    x = x0
    y = y0
    for _ in range(number_y):
        polygons.extend(aligned_nested_squares(x, y, side0, spacing, depth, number_x))
        y += 2 * depth * spacing
    return polygons

def squares_fractal(x0: float, y0: float, side0: float, depth: int):
    """
    create a fractal pattern of squares.
    """
    spacing = 0.05 * side0
    if depth == 0:
        return []
    else:
        polygons = []
        polygons.append(square(x0, y0, side0))
        polygons.extend(squares_fractal(x0 + side0/4, y0 + side0/4, side0 / 4, depth - 1))
        polygons.extend(squares_fractal(x0 + 2*side0/4 + spacing, y0 + 2*side0/4 + spacing, side0 / 4, depth - 1))
        polygons.extend(squares_fractal(x0 + side0/4, y0 + 2*side0/4 + spacing, side0 / 4, depth - 1))
        polygons.extend(squares_fractal(x0 + 2*side0/4 + spacing,  y0 +side0/4, side0 / 4, depth - 1))
        return polygons 

############################################################################################################

def polygon_center(polygon: Polygon):
    """
    return the center of a polygon.
    """
    x = 0
    y = 0
    for point in polygon.points:
        x += point.coordinates[0]
        y += point.coordinates[1]
    return Point([x / len(polygon.points), y / len(polygon.points)])

def is_convex(polygon: Polygon):
    """
    check if a polygon is convex.
    """
    for i in range(len(polygon.points)):
        p1 = polygon.points[i]
        p2 = polygon.points[(i + 1) % len(polygon.points)]
        p3 = polygon.points[(i + 2) % len(polygon.points)]
        cross_product = (p2.coordinates[0] - p1.coordinates[0]) * (p3.coordinates[1] - p2.coordinates[1]) - (p2.coordinates[1] - p1.coordinates[1]) * (p3.coordinates[0] - p2.coordinates[0])
        if cross_product < 0:
            return False
    return True

def rotate_polygon(polygon: Polygon, angle: float):
    """
    rotate a polygon by an angle.
    """
    center = polygon_center(polygon)
    new_points = []
    for point in polygon.points:
        x = point.coordinates[0]
        y = point.coordinates[1]
        x -= center.coordinates[0]
        y -= center.coordinates[1]
        new_x = x * cos(angle) - y * sin(angle)
        new_y = x * sin(angle) + y * cos(angle)
        new_x += center.coordinates[0]
        new_y += center.coordinates[1]
        new_points.append(Point([new_x, new_y]))
    return Polygon(new_points)

def translate_polygon(polygon: Polygon, x: float, y: float):
    """
    translate a polygon by a vector.
    """
    new_points = []
    for point in polygon.points:
        new_points.append(Point([point.coordinates[0] + x, point.coordinates[1] + y]))
    return Polygon(new_points)

############################################################################################################

def grid_points(x0: float, y0: float, step: float, n: int):
    """
    create a grid of points.
    """
    for i in range(n):
        for j in range(n):
            yield Point([x0 + i * step, y0 + j * step])

BASIC_GRID = list(grid_points(0, 0, 1, 10*(100)))

############################################################################################################

def random_triangle_in_grid(grid: list):
    """
    create a random triangle in a grid.
    """
    points = random.sample(grid, 3)
    return Polygon(points)

def points_inside_polygon(polygon: Polygon, grid: list):
    """
    return the points inside a polygon.
    """
    for point in grid:
        if ray_casting.point_in_polygon(point, polygon):
            yield point

def random_triangles_in_grid(grid: list, number: int):
    """
    create random un intersecting triangles in a grid.
    """
    polygons = []
    polygon = random_triangle_in_grid(grid)
    new_grid = list(points_inside_polygon(polygon, grid))
    polygons.append(polygon)
    while len(new_grid) >= 3 and len(polygons) < number:
        polygon = random_triangle_in_grid(new_grid)
        new_grid = list(points_inside_polygon(polygon, new_grid))
        polygons.append(polygon)

    return polygons

def max_x_triangle(polygons : list):
    """
    return the highest x value of all the triangles.
    """
    max_x = 0
    for polygon in polygons:
        for point in polygon.points:
            if point.coordinates[0] > max_x:
                max_x = point.coordinates[0]
    return max_x

def max_y_triangle(polygons : list):
    """
    return the highest y value of all the triangles.
    """
    max_y = 0
    for polygon in polygons:
        for point in polygon.points:
            if point.coordinates[1] > max_y:
                max_y = point.coordinates[1]
    return max_y

def random_polygon_using_unit_circle(n: int, radius: float):
    """
    create a random polygon using the unit circle.
    """
    points = []
    for i in range(n):
        angle = 2 * 3.14159265359 * i / n
        x = radius * cos(angle)
        y = radius * sin(angle)
        points.append(Point([x, y]))
    return Polygon(points)

def get_inscribed_circle_radius(polygon: Polygon):
    """
    return the radius of the inscribed circle of a polygon.
    """
    radius = float('inf')
    for i in range(len(polygon.points)):
        p1 = polygon.points[i]
        p2 = polygon.points[(i + 1) % len(polygon.points)]
        p3 = polygon.points[(i + 2) % len(polygon.points)]
        a = p1.distance_to(p2)
        b = p2.distance_to(p3)
        c = p3.distance_to(p1)
        s = (a + b + c) / 2
        r = (s * (s - a) * (s - b) * (s - c)) ** 0.5 / s
        if r < radius:
            radius = r
    return r

def nested_polygons_using_unit_circle(n: int, radius: float, depth: int):
    """
    create a nested pattern of triangles using the unit circle.
    """
    assert n >= 3, "n must be greater than or equal to 3"
    polygons = []
    new_radius = radius
    num_points = random.randint(3, n)
    polygons.append(random_polygon_using_unit_circle(num_points, radius))
    for i in range(1, depth):
        num_points = random.randint(3, n)
        new_radius = (new_radius - get_inscribed_circle_radius(polygons[-1])) * 0.9
        polygons.append(rotate_polygon(random_polygon_using_unit_circle(num_points, new_radius), random.uniform(0, PI)))
    return polygons

def generate_random_nested_polygons_components(x: int, y: int, n: int, radius: float, depth: int):
    """
    generate x * y random nested components. (translated with min distance of radius)
    """
    polygons = []
    for i in range(x):
        for j in range(y):
            new_polygons = nested_polygons_using_unit_circle(n, radius, depth)
            for polygon in new_polygons:
                polygons.append(translate_polygon(polygon, i * 3 * radius, j * 3 * radius))
    return polygons

def generate_random_handmade_components(x: int, y: int):
    """
    generate x * y random handmade components.
    """
    polygons = []
    for i in range(x):
        for j in range(y):
            new_polygons = HANDMADE_POLYGONS
            for polygon in new_polygons:
                polygons.append(translate_polygon(polygon, i * 125, j * 125))
    return polygons

############################################################################################################

import os

def generate_poly_test_file(polygons: list, filename: str):
    """
    generate a test file with the polygons
    with on each line first the index of the polygon and then the coordinates of the points.
    """
    directory = 'rendu_code/test_files/'
    
    # if the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # if the file already exists, we erase it
    with open(directory + filename, 'w') as file:
        for i in range(len(polygons)):
            for point in polygons[i].points:
                file.write(str(i) + ' ' + str(point.coordinates[0]) + ' ' + str(point.coordinates[1]) + ' \n')
############################################################################################################

def main():
    """
    main function, used to test the functions.
    """
    generate_poly_test_file(generate_random_handmade_components(5, 5), 'handmade_test.poly')

if __name__ == "__main__":
    main()