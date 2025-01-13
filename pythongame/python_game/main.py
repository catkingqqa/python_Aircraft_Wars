import turtle
import pyautogui
import time
from player import Player
from enemy import Enemy

turtle.register_shape('player.gif')

class Game:
    def __init__(self):
        # 初始化遊戲畫面
        self.screen = turtle.Screen()
        self.screen.setup(width=1280, height=960)
        self.screen.bgpic('background.gif')
        self.screen.tracer(0)
        self.screen.listen()

        # 初始化玩家
        self.player = Player('player.gif', 'black', 0, -350)
        self.player_health = 100  # 玩家血量

        # 初始化敵人
        self.enemies = []
        self.spawn_enemy_interval = 2
        self.last_spawn_time = time.time()

        # 顯示血量
        self.health_display = turtle.Turtle()
        self.health_display.hideturtle()
        self.health_display.penup()
        self.health_display.color("white")  
        self.health_display.goto(-500, 400)  # 設置位置為 (-300, 500)
        self.update_health_display()

        # 綁定鍵盤事件
        self.screen.onkey(self.player.shoot, "space")  # 按空白鍵發射子彈

        # 開始遊戲循環
        self.run_game()

    def run_game(self):
        while True:
            # 獲取滑鼠位置並更新玩家位置
            x, _ = pyautogui.position()
            mapped_x = self.map_mouse_to_screen(x)
            self.player.setx(self.limit_position(mapped_x))

            # 更新玩家狀態
            self.player.update()

            # 生成敵人
            self.spawn_enemies()

            # 更新敵人狀態
            self.update_enemies()

            # 檢查碰撞
            self.check_collisions()

            # 更新畫面
            self.screen.update()
            time.sleep(0.01)

    def map_mouse_to_screen(self, x):
        screen_width = 1920
        game_width = self.screen.window_width()
        return (x / screen_width) * game_width - game_width / 2

    def limit_position(self, x):
        half_width = self.screen.window_width() / 2
        return max(-half_width + 25, min(half_width - 25, x))

    def spawn_enemies(self):
        current_time = time.time()
        if current_time - self.last_spawn_time >= self.spawn_enemy_interval:
            enemy = Enemy()
            self.enemies.append(enemy)
            self.last_spawn_time = current_time

    def update_enemies(self):
        for enemy in self.enemies[:]:
            enemy.move()
            enemy.shoot()
            enemy.update_bullets()

            if enemy.is_off_screen():
                self.remove_enemy(enemy)

    def check_collisions(self):
        # 玩家子彈命中敵人
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.distance(enemy) < 20:
                    bullet.hideturtle()
                    self.player.bullets.remove(bullet)
                    self.remove_enemy(enemy)

        # 敵人子彈命中玩家
        for enemy in self.enemies:
            for bullet in enemy.bullets[:]:
                if self.check_player_collision(bullet):
                    bullet.hideturtle()
                    enemy.bullets.remove(bullet)
                    self.reduce_player_health(10)

    def check_player_collision(self, bullet):
        """檢查玩家與子彈的碰撞"""
        player_left = self.player.xcor() - 80  
        player_right = self.player.xcor() + 80
        player_top = self.player.ycor() + 20
        player_bottom = self.player.ycor() - 20

        bullet_x = bullet.xcor()
        bullet_y = bullet.ycor()

        return (
            player_left <= bullet_x <= player_right and
            player_bottom <= bullet_y <= player_top
        )

    def reduce_player_health(self, amount):
        """減少玩家血量"""
        self.player_health -= amount
        self.update_health_display()
        if self.player_health <= 0:
            print("Game Over!")
            self.screen.bye()

    def update_health_display(self):
        """更新血量顯示"""
        self.health_display.clear()
        self.health_display.write(
            f"Health: {self.player_health}", align="left", font=("Arial", 16, "normal")
        )

    def remove_enemy(self, enemy):
        enemy.hideturtle()
        for bullet in enemy.bullets:
            bullet.hideturtle()
        self.enemies.remove(enemy)

if __name__ == "__main__":
    game = Game()
