import math

# Calculate the total area of:
# - Circle with diameter 3
# - Square with side 4
# - Rectangle with sides 3 and 5
# - Circle with diameter 7

def hello_world():
    print('Hello world')

hello_world()

def circle_area(diameter):
    return math.pow(diameter / 2, 2) * math.pi

circle_1_area = circle_area(3)
square = 4 * 4
rectangle = 3 * 5
circle_2_area = circle_area(7)
total_area = circle_1_area + square + rectangle + circle_2_area

# Object oriented variant
class Circle:
    def __init__(self, diameter=-1, radius=-1):
        if radius > 0:
            self.radius = radius
        elif diameter > 0:
            self.radius = diameter / 2
        else:
            print('Error: you need to specify either the diameter or radius')
    
    def area(self):
        return math.pow(self.radius, 2) * math.pi
    
    def __str__(self):
        return f'Circle with radius {self.radius}'

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def __str__(self):
        return f'Rectangle of {self.width} x {self.height}'

class Square(Rectangle):
    def __init__(self, side):
        self.width = side
        self.height = side

# circle = Circle(radius=1.5)
shapes = [
    Circle(radius=1.5),
    Rectangle(3, 5),
    Square(4)
]

for shape in shapes:
    print(shape)
    print(shape.area())
