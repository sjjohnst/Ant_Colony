import math
import random


class Vector:

    def __init__(self, x=0, y=0):

        self.x = x
        self.y = y

    def normalize(self):
        m = self.magnitude()
        if m != 0:
            self.x = self.x / m
            self.y = self.y / m
        return self

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def angle(self):
        if self.x == 0:
            theta = math.atan(math.inf*self.y)
        else:
            theta = math.atan(self.y/self.x)
        return theta

    def get_coord(self):
        return (self.x, self.y)

    def get_polar(self):
        theta = self.angle()
        m = self.magnitude()
        return (m, theta)

    def scale(self, s):
        self.x = self.x * s
        self.y = self.y * s
        return self

    def clamp(self, max_m):
        m = self.magnitude()
        if m > max_m:
            f = max_m / m
        else:
            f = 1.0
        self.x = f*self.x
        self.y = f*self.y
        return self

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

    def __mul__(self, s):
        self.x = self.x * s
        self.y = self.y * s
        return self

    def __floordiv__(self, s):
        self.x = self.x // s
        self.y = self.y // s
        return self

    def int(self):
        self.x = int(self.x)
        self.y = int(self.y)
        return self


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


def rand_inUnitCircle():
    z = random.uniform(0, 1)
    theta = (2.0 * math.pi) * z

    r = random.uniform(0, 1)

    x = r*math.cos(theta)
    y = r*math.sin(theta)

    return Vector(x, y)
