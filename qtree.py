import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random


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

    def __init__(self, top_left: Point, bot_right: Point):
        self.top_left = top_left
        self.bot_right = bot_right

        step_x = (self.bot_right.x - self.top_left.x)/2
        step_y = (self.bot_right.y - self.top_left.y)/2

        cx = self.top_left.x + step_x
        cy = self.top_left.y + step_y
        self.center = Point(cx, cy)

    def __str__(self):
        return f'top_left: {self.top_left} \nbot_right: {self.bot_right}'

    def contains(self, p: Point):
        in_x = self.top_left.x <= p.x <= self.bot_right.x
        in_y = self.top_left.y <= p.y <= self.bot_right.y
        return in_x and in_y

    def intersects(self, b):
        pass


# Use a Quadtree for now, maybe change to R-tree if performance is an issue with Quadtree
class QTree:
    """ A class implementing a Quad Tree. """

    def __init__(self, boundary: Box):
        self.node_capacity = 4

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

    def insert(self, p: Point):
        # ignore points that cannot be placed in this QTree boundary
        if not self.box.contains(p):
            return False

        # If there is still space in this QTree, add it
        if len(self.points) < self.node_capacity:
            self.points.append(p)
            return True

        # Otherwise, check if we need to subdivide into new QTree quadrants,
        # then add to whichever quadrant will take it
        if self.divided is False:
            self.subdivide()
            self.divided = True

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

    def plot(self, ax):
        # Get the rectangle corner and the height/width
        anchor_x = self.box.top_left.x
        anchor_y = self.box.top_left.y

        step_x = self.box.bot_right.x - self.box.top_left.x
        step_y = self.box.bot_right.y - self.box.top_left.y

        # Plot the boundary rectangle
        ax.add_patch(Rectangle((anchor_x, anchor_y), step_x, step_y,
                     edgecolor='black',
                     fill=False))

        # Plot all the points in this node
        for point in self.points:
            point.plot(ax)

        # Plot the children, if they exist
        if self.north_east is None:
            pass
        else:
            self.north_east.plot(ax)
            self.north_west.plot(ax)
            self.south_west.plot(ax)
            self.south_east.plot(ax)

    def show(self, screen):
        # Display all the items stored in this QTree onto a pygame display
        for point in self.points:
            point.show(screen)

        if self.divided:
            self.north_east.show(screen)
            self.north_west.show(screen)
            self.south_west.show(screen)
            self.south_east.show(screen)

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
