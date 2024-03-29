import math
import numpy as np
import pygame
from pygame.math import Vector2

class Vector:

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        self.payload = None
        self.time = None

    def normalize(self):
        m = self.magnitude()
        self.x = self.x / m
        self.y = self.y / m

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def angle(self):
        return math.atan(self.y/self.x)

    def get_coord(self):
        return (self.x, self.y)

    def get_polar(self):
        theta = self.angle()
        m = self.magnitude()
        return (m, theta)

    def scale(self, s):
        self.x = self.x * s
        self.y = self.y * s

    def clamp(self, max_m):
        m = self.magnitude()
        if m > max_m:
            self.normalize()
            self.scale(max_m)
        else:
            pass

    def distance_to(self, other):
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)

    def rotate(self, theta):
        # Rotate the vector by theta radians, counterclockwise
        rotation_matrix = np.array([[math.cos(theta), -math.sin(theta)],
                                    [math.sin(theta), math.cos(theta)]])
        old_point = np.array([self.x, self.y])
        new_point = np.matmul(rotation_matrix, old_point)
        self.x = new_point[0]
        self.y = new_point[1]

    def __add__(self, other):
        new = Vector()
        new.x = self.x + other.x
        new.y = self.y + other.y
        return new

    def __sub__(self, other):
        new = Vector()
        new.x = self.x - other.x
        new.y = self.y - other.y
        return new

    def __mul__(self, scalar: float):
        new = Vector()
        new.x = self.x * scalar
        new.y = self.y * scalar
        return new

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def dot(v1: Vector, v2: Vector) -> float:
    return v1.x*v2.x + v1.y*v2.y


def slerp(v1: Vector, v2: Vector, t: float) -> Vector:
    v1.normalize()
    v2.normalize()

    theta = angle(v1, v2)
    sin_theta = math.sin(theta)

    a = math.sin((1 - t) * theta) / sin_theta
    b = math.sin(t * theta) / sin_theta

    v1.scale(a)
    v2.scale(b)

    return v1 + v2


def angle(v1: Vector, v2: Vector) -> float:
    dot_product = dot(v1, v2)

    mod_of_v1 = v1.magnitude() * v2.magnitude()
    theta = dot_product/mod_of_v1

    return theta


class Box:
    """ Bounding box class """

    def __init__(self, top_left: Vector, bot_right: Vector):
        self.top_left = top_left
        self.bot_right = bot_right

        step_x = (self.bot_right.x - self.top_left.x)/2
        step_y = (self.bot_right.y - self.top_left.y)/2

        cx = self.top_left.x + step_x
        cy = self.top_left.y + step_y
        self.center = Vector2(cx, cy)

    def __str__(self):
        return f'top_left: {self.top_left} \nbot_right: {self.bot_right}'

    def contains(self, p: Vector2):
        in_x = self.top_left.x <= p.x <= self.bot_right.x
        in_y = self.top_left.y <= p.y <= self.bot_right.y
        return in_x and in_y

    def intersects(self, B):
        xminA = self.top_left.x
        xmaxA = self.bot_right.x
        yminA = self.top_left.y
        ymaxA = self.bot_right.y

        xminB = B.top_left.x
        xmaxB = B.bot_right.x
        yminB = B.top_left.y
        ymaxB = B.bot_right.y

        x_overlap = xmaxA >= xminB and xmaxB >= xminA
        y_overlap = ymaxA >= yminB and ymaxB >= yminA
        return x_overlap and y_overlap


# this is because dict.setdefault does not work.
def dict_setdefault(D, k, d):
    # D.setdefault(k[,d]) -&gt; D.get(k,d), also set D[k]=d if k not in D
    r = D.get(k,d)
    if k not in D:
        D[k] = d
    return r


class HashMap(object):
    """
    Hashmap is a spatial index which can be used for a broad-phase
    collision detection strategy.
    """

    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = {}

    def key(self, point):
        cell_size = self.cell_size
        return (
            int((math.floor(point[0] / cell_size)) * cell_size),
            int((math.floor(point[1] / cell_size)) * cell_size)
        )

    def insert(self, point: Vector2):
        """
        Insert point into the hashmap.
        """
        # self.grid.setdefault(self.key(point), []).append(point)
        self.grid.setdefault(self.key((point.x, point.y)), []).append(point)

    def delete(self, point: Vector2):
        """
        Delete point in the hashmap
        """
        points = self.grid.setdefault(self.key((point.x, point.y)), [])
        for i, p in enumerate(points):
            if p == point:
                del points[i]
                break

    def query_vec(self, point: Vector2):
        """
        Return all objects in the cell specified by point.
        """
        return self.grid.setdefault(self.key((point.x, point.y)), [])

    def query_point(self, point: tuple):
        """
        Return all objects in the cell specified by point
        """
        return self.grid.setdefault(self.key(point), [])

    def query_box(self, boundary: Box):
        """
        Return all objects that are in cells intersecting the box
        """
        top_left = boundary.top_left
        bot_right = boundary.bot_right

        # Generate spatial index keys for all box corners
        top_left_key = self.key((top_left.x, top_left.y))
        bot_right_key = self.key((bot_right.x, bot_right.y))

        # Iterate over all possible keys within the box, and add their contained points to the list
        minx, miny = top_left_key
        maxx, maxy = bot_right_key

        points = []
        for i in range(minx, maxx+1):
            for j in range(miny, maxy+1):
                # print(self.key((i, j)))
                points = points + self.query_point((i, j))

        return points

    def query_radius(self, centre, radius):
        minx = centre.x - radius
        miny = centre.y - radius
        maxx = centre.x + radius
        maxy = centre.y + radius
        points = self.query_box(Box(Vector(minx, miny), Vector(maxx, maxy)))

        return [p for p in points if centre.distance_to(p) <= radius]


class QTree:
    """ A class implementing a Quad Tree. """

    def __init__(self, boundary: Box):
        self.max_points = 10

        # This QTree nodes boundary
        self.box = boundary

        # List of point objects contained in this QTree node. Maximum of node_capacity
        self.points = []
        self.divided = False

    def search(self, p):
        # Find if point p exists in this quadtree
        if not self.box.contains(p):
            return False

        # Check all points in this quadtree
        if len(self.points) > 0:
            for d in self.points:
                if d.x == p.x and d.y == p.y:
                    return True

        # Check all points in sub trees
        if self.divided:
            return (self.nw.search(p) or
                    self.ne.search(p) or
                    self.sw.search(p) or
                    self.se.search(p))

        # No point found
        else:
            return False

    def insert(self, point):
        # ignore points that cannot be placed in this QTree
        if not self.box.contains(point) or self.search(point):
            return False

        # If there is still space in this QTree, add it
        if len(self.points) < self.max_points:
            self.points.append(point)
            return True

        # No room: divide into sub-trees if possible
        if self.divided is False:
            self.subdivide()

        # Try inserting into sub-trees
        return (self.ne.insert(point) or
                self.nw.insert(point) or
                self.se.insert(point) or
                self.sw.insert(point))

    def __len__(self):
        sub_len = 0
        if self.divided:
            sub_len = len(self.nw) + len(self.ne) + len(self.sw) + len(self.se)
        return len(self.points) + sub_len

    def empty(self):
        return len(self) == 0

    def delete(self, point):
        # If the point is not in this box then
        if not self.box.contains(point):
            return False

        for i, d in enumerate(self.points):
            if d.x == point.x and d.y == point.y:
                # We have found the point
                del self.points[i]
                return True

        if self.divided:
            deleted = (self.nw.delete(point) or
                       self.ne.delete(point) or
                       self.sw.delete(point) or
                       self.se.delete(point))

            # Check if all children are now empty
            if self.nw.empty() and self.ne.empty() and self.sw.empty() and self.se.empty():
                self.divided = False
                del self.nw
                del self.ne
                del self.sw
                del self.se

            return deleted

        else:
            # We checked all the points and none are the one we are looking for
            return False

    def subdivide(self):
        # Get the x and y steps from center to edges
        step_x = (self.box.center.x - self.box.top_left.x)
        step_y = (self.box.center.y - self.box.top_left.y)

        # Create new boundary points
        center_bottom = Vector(self.box.center.x, self.box.center.y+step_y)
        center_top    = Vector(self.box.center.x, self.box.center.y-step_y)
        center_left   = Vector(self.box.center.x-step_x, self.box.center.y)
        center_right  = Vector(self.box.center.x+step_x, self.box.center.y)

        # Create the new boundaries and QTree nodes
        self.nw = QTree(Box(self.box.top_left, self.box.center))
        self.ne = QTree(Box(center_top, center_right))
        self.se = QTree(Box(self.box.center, self.box.bot_right))
        self.sw = QTree(Box(center_left, center_bottom))

        self.divided = True

    def query_circle(self, boundary, centre, radius, found_points):
        """Find the points in the quadtree that lie within radius of centre.

        boundary is a Box object (a square) that bounds the search circle.
        There is no need to call this method directly: use query_radius.
        """

        if not self.box.intersects(boundary):
            # If the domain of this node does not intersect the search
            # region, we don't need to look in it for points.
            return False

        # Search this node's points to see if they lie within boundary
        # and also lie within a circle of given radius around the centre point.
        for point in self.points:
            if (boundary.contains(point) and
                    point.distance_to(centre) <= radius):
                found_points.append(point)

        # Recurse the search into this node's children.
        if self.divided:
            self.nw.query_circle(boundary, centre, radius, found_points)
            self.ne.query_circle(boundary, centre, radius, found_points)
            self.se.query_circle(boundary, centre, radius, found_points)
            self.sw.query_circle(boundary, centre, radius, found_points)

        return found_points

    def query_radius(self, centre, radius, found_points):
        """Find the points in the quadtree that lie within radius of centre."""

        # First find the square that bounds the search circle as a Rect object.
        top_left = Vector(centre.x - radius, centre.y - radius)
        bot_right = Vector(centre.x + radius, centre.y + radius)
        boundary = Box(top_left, bot_right)

        return self.query_circle(boundary, centre, radius, found_points)


# hmap = HashMap(1.0)
#
# hmap.insert(Vector(0.3, 0.6))
# hmap.insert(Vector(1.5, 2.3))
# hmap.insert(Vector(2.2, 2.5))
# hmap.insert(Vector(4.2, 5.0))
# hmap.insert(Vector(4.3, 5.2))
#
# # print(hmap.key((1.3, 0.6)))
#
# bound = Box(Vector(0.3, 1.3), Vector(3.2, 3.4))
# #
# # p = hmap.query_point((4.3, 5.1))
# # print([x.get_coord() for x in p])
#
# # points = hmap.query_box(bound)
# points = hmap.query_radius(Vector(1.3, 2.3), 5.0)
# for p in points:
#     print(p.get_coord())
