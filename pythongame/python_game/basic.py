import turtle

class Basic(turtle.Turtle):
    def __init__(self, shape, color, x, y):
        super().__init__(shape=shape)
        self.color(color)
        self.speed(0)
        self.penup()
        self.goto(x, y)
