from parameters import *


class Point:
    """ A point located at (x,y) in 2D space.
    Each Point object may be associated with a payload object.
    """
    def __init__(self, x, y, payload=None):
        self.x = x
        self.y = y
        self.payload = payload


# Use a Quadtree for now, maybe change to R-tree if performance is an issue with Quadtree
class QTree:
    """ A class implementing a Quad Tree. """

    def __init__(self, topL: Point, botR: Point):
        # Define the boundary box of this node
        self.topLeft = topL
        self.botRight = botR

        # Store details of the node
        self.node = None

        # Children of this tree
        self.topLeftTree = None
        self.topRightTree = None
        self.botLeftTree = None
        self.botRightTree = None

    def inBoundary(self, p: Point):
        """ Return true if p is within the boundary of this tree Node """
        return p.x >= self.topLeft.x and p.x <= self.botRight.x and p.y >= self.topLeft.y and p.y <= self.botRight.y

    def insert(self, p: Point):
        """ Insert point p into the quadtree (if possible) """

        pass