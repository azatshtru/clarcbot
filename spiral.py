import math

class Point(object):

    def __init__(self, x, y, a=0, b=1):
        self.x = x
        self.y = y

        self.r = math.sqrt(x*x + y*y)
        self.theta = math.atan2(y, x)

        self.a = a
        self.b = b

    def inc(self, deltatheta):
        self.r += self.a + (self.b * deltatheta)
        self.theta += deltatheta

        self.x = self.r * math.cos(self.theta)
        self.y = self.r * math.sin(self.theta)