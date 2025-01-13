import turtle
import random
import time
from bullet import Bullet

class Enemy(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.setposition(random.randint(-300, 300), random.randint(200, 450))  # 隨機生成敵人位置
        self.dx = random.choice([-2, 2])  # 水平移動速度
        self.bullets = []  # 儲存敵人的子彈
        self.shoot_interval = random.uniform(1, 3)  # 隨機發射間隔
        self.last_shot_time = time.time()

    def move(self):
        """更新敵人的隨機移動位置"""
        new_x = self.xcor() + self.dx
        if new_x > 400 or new_x < -400:  # 碰到邊界反向
            self.dx = -self.dx
        self.setx(new_x)

    def shoot(self):
        """敵人發射子彈"""
        current_time = time.time()
        if current_time - self.last_shot_time >= self.shoot_interval:
            bullet = Bullet(self.xcor(), self.ycor() - 20)  # 子彈從敵人下方發射
            bullet.dy = -10  # 子彈向下移動
            bullet.color("purple")  # 敵人子彈顏色
            self.bullets.append(bullet)
            self.last_shot_time = current_time

    def update_bullets(self):
        """更新敵人的子彈狀態"""
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen(960):  # 子彈超出畫面
                bullet.hideturtle()
                self.bullets.remove(bullet)

    def is_off_screen(self):
        """檢查敵人是否超出畫面"""
        return self.ycor() < -500 or self.ycor() > 500 or self.xcor() < -500 or self.xcor() > 500
