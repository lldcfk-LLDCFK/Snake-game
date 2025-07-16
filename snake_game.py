import pygame
import random
import sys
import os
import math
import tkinter as tk
from tkinter import messagebox

# 初始化 Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# 设置游戏窗口
WINDOW_WIDTH = 800   # 改回原来的窗口宽度
WINDOW_HEIGHT = 600  # 改回原来的窗口高度
BLOCK_SIZE = 25     # 增加方块大小
GAME_SPEED = 15
FOOD_COUNT = 2      # 修改食物数量为2个

# 定义方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇游戏')

# 初始化时钟
clock = pygame.time.Clock()

# 设置字体
FONT_DIR = "D:\\gameFONTS"
DEFAULT_FONT = os.path.join(FONT_DIR, "msyh.ttc")

# 确保字体目录存在
if not os.path.exists(FONT_DIR):
    os.makedirs(FONT_DIR)

def get_available_fonts():
    """获取字体目录中的所有字体文件"""
    fonts = []
    if os.path.exists(FONT_DIR):
        for file in os.listdir(FONT_DIR):
            if file.lower().endswith(('.ttf', '.ttc')):
                fonts.append(os.path.join(FONT_DIR, file))
    return fonts

def load_font(font_path, size=36):
    """加载字体文件"""
    try:
        if os.path.exists(font_path):
            print(f"正在加载字体: {font_path}")
            return pygame.font.Font(font_path, size)
        else:
            print(f"字体文件不存在: {font_path}")
            return pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', size)
    except Exception as e:
        print(f"加载字体时出错: {str(e)}")
        return pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', size)

# 获取可用字体列表
available_fonts = get_available_fonts()
current_font_index = 0

# 加载初始字体
game_font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 36)
if available_fonts:
    loaded_font = load_font(available_fonts[0])
    if loaded_font:
        game_font = loaded_font
        print(f"已加载字体: {available_fonts[0]}")
else:
    print("未找到字体文件，使用系统默认字体")

class Snake:
    def __init__(self, color, is_ai=False):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = color
        self.score = 0
        self.is_ai = is_ai
        self.growing = False

    def get_head_position(self):
        return self.positions[0]

    def get_next_position(self):
        """获取下一个位置"""
        cur = self.get_head_position()
        x, y = self.direction
        return ((cur[0] + (x*BLOCK_SIZE)) % WINDOW_WIDTH, 
                (cur[1] + (y*BLOCK_SIZE)) % WINDOW_HEIGHT)

    def update(self):
        next_pos = self.get_next_position()
        
        # 检查是否撞到自己
        if next_pos in self.positions[3:]:
            return False
            
        # 移动蛇
        self.positions.insert(0, next_pos)
        if not self.growing:
            self.positions.pop()
        else:
            self.growing = False
        return True

    def grow(self):
        """让蛇变长"""
        self.growing = True
        self.length += 1
        self.score += 1

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.growing = False

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

    def ai_move(self, foods):
        if not self.is_ai or not foods:
            return

        # 找到最近的食物
        head = self.get_head_position()
        nearest_food = min(foods, key=lambda food: math.sqrt(
            (head[0] - food.position[0])**2 + 
            (head[1] - food.position[1])**2
        ))

        # 计算到食物的方向
        dx = nearest_food.position[0] - head[0]
        dy = nearest_food.position[1] - head[1]

        # 确定移动方向
        if abs(dx) > abs(dy):
            if dx > 0 and self.direction != LEFT:
                self.direction = RIGHT
            elif dx < 0 and self.direction != RIGHT:
                self.direction = LEFT
        else:
            if dy > 0 and self.direction != UP:
                self.direction = DOWN
            elif dy < 0 and self.direction != DOWN:
                self.direction = UP

class Food:
    def __init__(self, color=None):
        self.position = (0, 0)
        self.color = color or random.choice([RED, YELLOW, PURPLE])
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
                        random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

def check_collision(pos1, pos2):
    """检查两个位置是否碰撞"""
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

def select_mode():
    mode = {'value': None}
    def set_mode(val):
        mode['value'] = val
        root.destroy()
    root = tk.Tk()
    root.title('选择游戏模式')
    root.geometry('320x260')
    tk.Label(root, text='请选择游戏模式', font=('Arial', 16)).pack(pady=20)
    tk.Button(root, text='经典模式', width=20, height=2, command=lambda: set_mode('classic')).pack(pady=5)
    tk.Button(root, text='双人对战', width=20, height=2, command=lambda: set_mode('versus')).pack(pady=5)
    tk.Button(root, text='障碍模式', width=20, height=2, command=lambda: set_mode('obstacle')).pack(pady=5)
    tk.Button(root, text='极速模式', width=20, height=2, command=lambda: set_mode('speed')).pack(pady=5)
    root.mainloop()
    return mode['value']

def main():
    global current_font_index, game_font, available_fonts
    mode = select_mode()
    if mode is None:
        sys.exit()
    # 下面根据mode分支进入不同玩法
    if mode == 'classic':
        return main_classic()
    elif mode == 'versus':
        return main_versus()
    elif mode == 'obstacle':
        return main_obstacle()
    elif mode == 'speed':
        return main_speed()
    else:
        sys.exit()

def main_classic():
    player = Snake(GREEN)
    opponent = Snake(BLUE, is_ai=True)
    foods = [Food() for _ in range(FOOD_COUNT)]
    gold_apple = Food(YELLOW)
    gold_timer = 0
    invincible = 0
    current_font = game_font
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.direction != DOWN:
                    player.direction = UP
                elif event.key == pygame.K_DOWN and player.direction != UP:
                    player.direction = DOWN
                elif event.key == pygame.K_LEFT and player.direction != RIGHT:
                    player.direction = LEFT
                elif event.key == pygame.K_RIGHT and player.direction != LEFT:
                    player.direction = RIGHT
                elif event.key == pygame.K_f:
                    if available_fonts:
                        current_font_index = (current_font_index + 1) % len(available_fonts)
                        new_font = load_font(available_fonts[current_font_index])
                        if new_font:
                            current_font = new_font
                            print(f"切换到字体: {available_fonts[current_font_index]}")

        # 检查是否吃到食物
        player_next_pos = player.get_next_position()
        opponent_next_pos = opponent.get_next_position()
        for food in foods[:]:
            if check_collision(player_next_pos, food.position):
                player.grow()
                foods.remove(food)
                foods.append(Food())
            elif check_collision(opponent.get_head_position(), food.position):
                opponent.grow()
                foods.remove(food)
                foods.append(Food())
        # 金苹果出现与判定
        gold_timer += 1
        show_gold = (gold_timer // 120) % 2 == 0
        if show_gold:
            gold_apple.render(screen)
            if check_collision(player.get_head_position(), gold_apple.position):
                player.score += 3
                invincible = 60  # 1秒无敌
                gold_apple.randomize_position()
        # 更新蛇的位置
        if not player.update():
            if invincible > 0:
                invincible -= 1
            else:
                player.reset()
                opponent.reset()
                foods = [Food() for _ in range(FOOD_COUNT)]
                gold_apple = Food(YELLOW)
                gold_timer = 0
                invincible = 0
        # AI移动
        opponent.ai_move(foods)
        if not opponent.update():
            opponent.reset()
        # 绘制游戏界面
        screen.fill(BLACK)
        player.render(screen)
        opponent.render(screen)
        for food in foods:
            food.render(screen)
        if show_gold:
            gold_apple.render(screen)
        # 显示分数
        player_score = current_font.render(f'玩家得分: {player.score}', True, WHITE)
        opponent_score = current_font.render(f'对手得分: {opponent.score}', True, WHITE)
        screen.blit(player_score, (20, 20))
        screen.blit(opponent_score, (20, 70))
        tip_text = current_font.render('按F键切换字体 金苹果=+3分&无敌', True, WHITE)
        screen.blit(tip_text, (20, 120))
        font_name = os.path.basename(available_fonts[current_font_index]) if available_fonts else "系统默认字体"
        font_info = current_font.render(f'当前字体: {font_name}', True, WHITE)
        screen.blit(font_info, (20, 170))
        pygame.display.update()
        clock.tick(GAME_SPEED)

def main_versus():
    player1 = Snake(GREEN)
    player2 = Snake(BLUE)
    foods = [Food() for _ in range(FOOD_COUNT)]
    special_food = Food(PURPLE)
    special_food_timer = 0
    current_font = game_font
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 玩家1：方向键
                if event.key == pygame.K_UP and player1.direction != DOWN:
                    player1.direction = UP
                elif event.key == pygame.K_DOWN and player1.direction != UP:
                    player1.direction = DOWN
                elif event.key == pygame.K_LEFT and player1.direction != RIGHT:
                    player1.direction = LEFT
                elif event.key == pygame.K_RIGHT and player1.direction != LEFT:
                    player1.direction = RIGHT
                # 玩家2：WSAD
                elif event.key == pygame.K_w and player2.direction != DOWN:
                    player2.direction = UP
                elif event.key == pygame.K_s and player2.direction != UP:
                    player2.direction = DOWN
                elif event.key == pygame.K_a and player2.direction != RIGHT:
                    player2.direction = LEFT
                elif event.key == pygame.K_d and player2.direction != LEFT:
                    player2.direction = RIGHT
        # 吃食物
        for food in foods[:]:
            if check_collision(player1.get_next_position(), food.position):
                player1.grow()
                foods.remove(food)
                foods.append(Food())
            elif check_collision(player2.get_next_position(), food.position):
                player2.grow()
                foods.remove(food)
                foods.append(Food())
        # 特殊食物出现与判定
        special_food_timer += 1
        show_special = (special_food_timer // 60) % 2 == 0
        if show_special:
            special_food.render(screen)
            if check_collision(player1.get_head_position(), special_food.position):
                # 反转player2方向
                player2.direction = (-player2.direction[0], -player2.direction[1])
                special_food.randomize_position()
            elif check_collision(player2.get_head_position(), special_food.position):
                player1.direction = (-player1.direction[0], -player1.direction[1])
                special_food.randomize_position()
        # 更新
        if not player1.update() or not player2.update():
            player1.reset()
            player2.reset()
            foods = [Food() for _ in range(FOOD_COUNT)]
            special_food = Food(PURPLE)
            special_food_timer = 0
        # 玩家碰撞对方身体判负
        if player1.get_head_position() in player2.positions[1:]:
            messagebox.showinfo('游戏结束', '玩家1撞到玩家2，玩家2获胜！')
            player1.reset(); player2.reset(); foods = [Food() for _ in range(FOOD_COUNT)]
        if player2.get_head_position() in player1.positions[1:]:
            messagebox.showinfo('游戏结束', '玩家2撞到玩家1，玩家1获胜！')
            player1.reset(); player2.reset(); foods = [Food() for _ in range(FOOD_COUNT)]
        # 绘制
        screen.fill(BLACK)
        player1.render(screen)
        player2.render(screen)
        for food in foods:
            food.render(screen)
        if show_special:
            special_food.render(screen)
        s1 = current_font.render(f'玩家1得分: {player1.score}', True, WHITE)
        s2 = current_font.render(f'玩家2得分: {player2.score}', True, WHITE)
        screen.blit(s1, (20, 20))
        screen.blit(s2, (20, 70))
        tip = current_font.render('玩家1:方向键 玩家2:WSAD 紫色食物=反转对方', True, WHITE)
        screen.blit(tip, (20, 120))
        pygame.display.update()
        clock.tick(GAME_SPEED)

def main_obstacle():
    # 障碍模式：随机生成障碍，碰撞即重置
    player = Snake(GREEN)
    foods = [Food() for _ in range(FOOD_COUNT)]
    obstacles = [(random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE,
                  random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE)
                 for _ in range(10)]
    current_font = game_font
    last_score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.direction != DOWN:
                    player.direction = UP
                elif event.key == pygame.K_DOWN and player.direction != UP:
                    player.direction = DOWN
                elif event.key == pygame.K_LEFT and player.direction != RIGHT:
                    player.direction = LEFT
                elif event.key == pygame.K_RIGHT and player.direction != LEFT:
                    player.direction = RIGHT
        # 吃食物
        for food in foods[:]:
            if check_collision(player.get_next_position(), food.position):
                player.grow()
                foods.remove(food)
                foods.append(Food())
        # 难度递增：每吃5个食物增加障碍
        if player.score > 0 and player.score % 5 == 0 and player.score != last_score:
            last_score = player.score
            # 新障碍不与蛇重叠
            while True:
                new_obs = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE,
                           random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE)
                if new_obs not in player.positions and new_obs not in obstacles:
                    obstacles.append(new_obs)
                    break
        # 更新
        if not player.update() or player.get_head_position() in obstacles:
            player.reset()
            foods = [Food() for _ in range(FOOD_COUNT)]
            obstacles = [(random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE,
                          random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE)
                         for _ in range(10)]
            last_score = 0
        # 绘制
        screen.fill(BLACK)
        player.render(screen)
        for food in foods:
            food.render(screen)
        for obs in obstacles:
            pygame.draw.rect(screen, RED, (obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))
        score = current_font.render(f'得分: {player.score}', True, WHITE)
        screen.blit(score, (20, 20))
        tip = current_font.render('障碍物每5分增加，碰撞即重置', True, WHITE)
        screen.blit(tip, (20, 70))
        pygame.display.update()
        clock.tick(GAME_SPEED)

def main_speed():
    # 极速模式：蛇移动速度更快
    player = Snake(GREEN)
    foods = [Food() for _ in range(FOOD_COUNT)]
    current_font = game_font
    fast_speed = GAME_SPEED * 2
    max_speed = GAME_SPEED * 4
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.direction != DOWN:
                    player.direction = UP
                elif event.key == pygame.K_DOWN and player.direction != UP:
                    player.direction = DOWN
                elif event.key == pygame.K_LEFT and player.direction != RIGHT:
                    player.direction = LEFT
                elif event.key == pygame.K_RIGHT and player.direction != LEFT:
                    player.direction = RIGHT
        # 吃食物
        for food in foods[:]:
            if check_collision(player.get_next_position(), food.position):
                player.grow()
                foods.remove(food)
                foods.append(Food())
                # 每吃3个食物速度提升
                if player.score % 3 == 0 and fast_speed < max_speed:
                    fast_speed += GAME_SPEED
        # 更新
        if not player.update():
            player.reset()
            foods = [Food() for _ in range(FOOD_COUNT)]
            fast_speed = GAME_SPEED * 2
        # 绘制
        screen.fill(BLACK)
        player.render(screen)
        for food in foods:
            food.render(screen)
        score = current_font.render(f'得分: {player.score}', True, WHITE)
        screen.blit(score, (20, 20))
        tip = current_font.render(f'极速模式，速度：{fast_speed//GAME_SPEED}倍', True, WHITE)
        screen.blit(tip, (20, 70))
        pygame.display.update()
        clock.tick(fast_speed)

if __name__ == '__main__':
    main()
