import turtle

class Bullet(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("circle")
        self.color("red")
        self.penup()
        self.speed(0)
        self.setposition(x, y)
        self.dy = 15  # 子彈移動速度

    def move(self):
        """更新子彈位置"""
        new_y = self.ycor() + self.dy
        self.sety(new_y)

    def is_off_screen(self, screen_height):
        """檢查子彈是否超出畫面"""
        return self.ycor() > screen_height / 2
