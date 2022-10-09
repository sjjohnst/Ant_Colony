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
        self.center = Point(cx, cy)

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
        self.node_capacity = 1

        # This QTree nodes boundary
        self.box = boundary

        # List of point objects contained in this QTree node. Maximum of node_capacity
        self.points = []
        self.divided = False

        # Children
        self.north_west = None
        self.north_east = None
        self.south_west = None
        self.south_east = None

    def search(self, p):
        # Find if point p exists in this quadtree
        if not self.box.contains(p):
            return False

        elif self.divided is True:
            # Recurse into the box that might hold the point
            if self.north_west.box.contains(p):
                return self.north_west.search(p)
            if self.north_east.box.contains(p):
                return self.north_east.search(p)
            if self.south_west.box.contains(p):
                return self.south_west.search(p)
            if self.south_east.box.contains(p):
                return self.south_east.search(p)

        elif len(self.points) > 0:
            for d in self.points:
                if d.x == p.x and d.y == p.y:
                    return True

        else:
            return False

    def insert(self, p):
        # ignore points that cannot be placed in this QTree boundary
        if not self.box.contains(p):
            return False

        if self.search(p) is True:
            return False

        # If there is still space in this QTree, add it
        if len(self.points) < self.node_capacity and self.divided is False:
            self.points.append(p)
            return True

        # Otherwise, check if we need to subdivide into new QTree quadrants,
        # then add to whichever quadrant will take it
        # Take point from this quad and insert into new child sections
        if self.divided is False:
            self.subdivide()
            self.divided = True

        if len(self.points) >= self.node_capacity:
            for i in range(len(self.points)):
                d = self.points[i]
                if self.north_west.insert(d): continue
                if self.north_east.insert(d): continue
                if self.south_west.insert(d): continue
                if self.south_east.insert(d): continue
            for i in range(len(self.points)):
                del self.points[i]

        # Insert point of interest
        if self.north_west.insert(p):
            return True
        if self.north_east.insert(p):
            return True
        if self.south_west.insert(p):
            return True
        if self.south_east.insert(p):
            return True

        # Else we cannot insert the point for some unknown reason (this should never happen)
        return False

    def subdivide(self):
        # Get the x and y steps from center to edges
        step_x = (self.box.center.x - self.box.top_left.x)
        step_y = (self.box.center.y - self.box.top_left.y)

        # Create new boundary points
        center_bottom = Point(self.box.center.x, self.box.center.y+step_y)
        center_top    = Point(self.box.center.x, self.box.center.y-step_y)
        center_left   = Point(self.box.center.x-step_x, self.box.center.y)
        center_right  = Point(self.box.center.x+step_x, self.box.center.y)

        # Create the new boundaries and QTree nodes
        self.north_west = QTree(Box(self.box.top_left, self.box.center))
        self.north_east = QTree(Box(center_top, center_right))
        self.south_east = QTree(Box(self.box.center, self.box.bot_right))
        self.south_west = QTree(Box(center_left, center_bottom))

    def nearest_point(self, p: Point):
        # Find the point in the Quadtree that is nearest to param p
        if len(self.points) > 0:
            min_dist = 0
            j = 0
            for i in range(len(self.points)):
                d = self.points[i]
                dist = math.sqrt((p.x - d.x)*(p.x - d.x) + (p.y - d.y)*(p.y - d.y))
                if min_dist == 0:
                    min_dist = dist
                elif min_dist < dist:
                    j = i
            return (self.points[j].x, self.points[j].y)

        elif self.divided is True:
            # p is in the box, but no points in this tree. Check children
            if self.north_west.box.contains(p):
                return self.north_west.nearest_point(p)
            elif self.north_east.box.contains(p):
                return self.north_east.nearest_point(p)
            elif self.south_west.box.contains(p):
                return self.south_west.nearest_point(p)
            elif self.south_east.box.contains(p):
                return self.south_east.nearest_point(p)
        else:
            return False

    def show(self, screen):
        # Display all the items stored in this QTree onto a pygame display
        if self.divided:
            self.north_east.show(screen)
            self.north_west.show(screen)
            self.south_west.show(screen)
            self.south_east.show(screen)

        else:
            for point in self.points:
                point.show(screen)

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
