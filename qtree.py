from matplotlib.patches import Rectangle
from vector import Vector
import math

class Point:
    """ A point located at (x,y) in 2D space.
    Each Point object may be associated with a payload object.
    """

    def __init__(self, x, y, payload=None):
        self.x = x
        self.y = y
        self.payload = payload

    def __str__(self):
        return f'({self.x}, {self.y})'

    def plot(self, ax):
        ax.scatter(self.x, self.y, color='blue')


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


def intersect(A: Box, B: Box):
    xminA = A.top_left.x
    xmaxA = A.bot_right.x
    yminA = A.top_left.y
    ymaxA = A.bot_right.y

    xminB = B.top_left.x
    xmaxB = B.bot_right.x
    yminB = B.top_left.y
    ymaxB = B.bot_right.y

    x_overlap = xmaxA >= xminB and xmaxB >= xmaxA
    y_overlap = ymaxA >= yminB and ymaxB >= ymaxA
    return x_overlap and y_overlap


# Use a Quadtree for now, maybe change to R-tree if performance is an issue with Quadtree
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

    def nearest_point(self, p: Point):
        # Find the point in the Quadtree that is nearest to param p
        pass

    def show(self, screen):
        # Display all the items stored in this QTree onto a pygame display
        for point in self.points:
            point.show(screen)

        if self.divided:
            self.ne.show(screen)
            self.nw.show(screen)
            self.sw.show(screen)
            self.se.show(screen)

# top_left = Point(0, 0)
# bot_right = Point(200, 200)
# box = Box(top_left, bot_right)
# tree = QTree(box)
#
# fig, ax = plt.subplots(1, 1, figsize=(10,10))
#
# num_points = 500
# for i in range(num_points):
#     x = random.randrange(0, 200)
#     y = random.randrange(0, 200)
#     p = Point(x, y)
#     tree.insert(p)
#
# tree.plot(ax)
#
# plt.show()
