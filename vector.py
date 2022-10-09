import math


class Vector:

    def __init__(self, x=0, y=0):

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
