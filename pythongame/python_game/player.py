from basic import Basic
from bullet import Bullet
import time

class Player(Basic):
    def __init__(self, shape, color, x, y):
        super().__init__(shape, color, x, y)
        self.shapesize(stretch_wid=5, stretch_len=5)
        self.dx = 10
        self.dy = 0
        self.gravity = -1
        self.state = 'ground'
        self.bullets = []  # 儲存所有子彈
        self.cooldown = 0.5  # 冷卻時間（秒）
        self.last_shot_time = 0  # 上次發射的時間

    def jump(self):
        """讓玩家跳躍"""
        if self.state == 'ground':
            self.dy = 20
            self.state = 'air'

    def shoot(self):
        """發射子彈，考慮冷卻時間"""
        current_time = time.time()
        if current_time - self.last_shot_time >= self.cooldown:
            bullet = Bullet(self.xcor(), self.ycor() + 20)  # 子彈從玩家頭頂發射
            self.bullets.append(bullet)
            self.last_shot_time = current_time  # 更新上次發射時間

    def update(self):
        """更新玩家狀態"""
        # 垂直運動
        self.dy += self.gravity
        new_y = self.ycor() + self.dy
        if new_y < -350:  # 假設地面位置是 -350
            new_y = -350
            self.dy = 0
            self.state = 'ground'
        self.sety(new_y)

        # 更新所有子彈
        for bullet in self.bullets[:]:
            bullet.move()
            # 移除超出畫面的子彈
            if bullet.is_off_screen(960):
                bullet.hideturtle()
                self.bullets.remove(bullet)
