import math


class Vector:

    def __init__(self, x=0.0, y=0.0):

        self.x = x
        self.y = y

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
        self.center = Vector(cx, cy)

    def __str__(self):
        return f'top_left: {self.top_left} \nbot_right: {self.bot_right}'

    def contains(self, p: Vector):
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


class QTree:
    """ A class implementing a Quad Tree. """

    def __init__(self, boundary: Box):
        self.max_points = 4

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

