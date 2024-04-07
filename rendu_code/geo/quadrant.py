"""
quadrants are rectangular boxes delimiting a set of items.
they are used in display to compute image sizes.
"""
from  itertools import product

class Quadrant:
    """
    enclosing rectangles.
    """
    def __init__(self, min_coordinates, max_coordinates):
        self.min_coordinates = list(min_coordinates)
        self.max_coordinates = list(max_coordinates)

    def copy(self):
        """
        return deepcopy of given quadrant.
        """
        return Quadrant(
            list(self.min_coordinates), list(self.max_coordinates))

    @classmethod
    def empty_quadrant(cls, dimension):
        """
        return an empty quadrant in space of given dimension
        """
        min_coordinates = []
        max_coordinates = []
        for _ in range(dimension):
            min_coordinates.append(float('+inf'))
            max_coordinates.append(float('-inf'))
        return cls(min_coordinates, max_coordinates)

    def add_point(self, added_point):
        """
        register a point inside the quadrant.
        update limits if needed.
        """
        for i, added_coordinate in enumerate(added_point.coordinates):
            if added_coordinate < self.min_coordinates[i]:
                self.min_coordinates[i] = added_coordinate
            if added_coordinate > self.max_coordinates[i]:
                self.max_coordinates[i] = added_coordinate

    def update(self, other):
        """
        expands self quadrant by taking constraints from other quadrant into account.
        the new one will have the minimal size needed to contain both initial ones.
        """
        assert len(self.min_coordinates) == len(other.min_coordinates), \
            'merge in different spaces'
        for i, coordinate in enumerate(other.min_coordinates):
            if self.min_coordinates[i] > coordinate:
                self.min_coordinates[i] = coordinate
        for i, coordinate in enumerate(other.max_coordinates):
            if self.max_coordinates[i] < coordinate:
                self.max_coordinates[i] = coordinate

    def limits(self, index):
        """
        returns array of limits for a given coordinate index
        """
        return (self.min_coordinates[index], self.max_coordinates[index])

    def intersect(self, other):
        """
        do we have any region in common ?
        """
        return all((mi1 < ma2 and ma1 > mi2) for mi1, mi2, ma1, ma2 in zip(self.min_coordinates, other.min_coordinates, self.max_coordinates, other.max_coordinates))

    def inflate(self, distance):
        """
        get bigger quadrant containing original one + any point outside
        original at distance less than given
        """
        self.min_coordinates = [c - distance for c in self.min_coordinates]
        self.max_coordinates = [c + distance for c in self.max_coordinates]

    def inflate_factor(self, factor):
        """
        get bigger quadrant by applying a multiplicative factor in each
        dimension, where 1 means "unchanged"
        """
        self.min_coordinates, self.max_coordinates = \
            zip(*[(cmin - (cmax - cmin) * (factor - 1) / 2,
                   cmax + (cmax - cmin) * (factor - 1) / 2)
                  for cmin, cmax in zip(self.min_coordinates, self.max_coordinates)])

    def get_arrays(self):
        """
        returns arrays of limits
        """
        return (self.min_coordinates, self.max_coordinates)
