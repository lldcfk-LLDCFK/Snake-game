import pygame
import random
import sys
import os
import math

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

def main():
    global current_font_index, game_font, available_fonts
    
    player = Snake(GREEN)
    opponent = Snake(BLUE, is_ai=True)
    foods = [Food() for _ in range(FOOD_COUNT)]
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
                print(f"玩家吃到食物！当前长度：{player.length}，得分：{player.score}")
            elif check_collision(opponent_next_pos, food.position):
                opponent.grow()
                foods.remove(food)
                foods.append(Food())
                print(f"对手吃到食物！当前长度：{opponent.length}，得分：{opponent.score}")

        # 更新蛇的位置
        if not player.update():
            player.reset()
            opponent.reset()
            foods = [Food() for _ in range(FOOD_COUNT)]

        # AI移动
        opponent.ai_move(foods)
        if not opponent.update():
            player.reset()
            opponent.reset()
            foods = [Food() for _ in range(FOOD_COUNT)]

        # 绘制游戏界面
        screen.fill(BLACK)
        player.render(screen)
        opponent.render(screen)
        for food in foods:
            food.render(screen)
        
        # 显示分数
        player_score = current_font.render(f'玩家得分: {player.score}', True, WHITE)
        opponent_score = current_font.render(f'对手得分: {opponent.score}', True, WHITE)
        screen.blit(player_score, (20, 20))
        screen.blit(opponent_score, (20, 70))

        # 显示操作提示
        tip_text = current_font.render('按F键切换字体', True, WHITE)
        screen.blit(tip_text, (20, 120))

        # 显示当前字体名称
        font_name = os.path.basename(available_fonts[current_font_index]) if available_fonts else "系统默认字体"
        font_info = current_font.render(f'当前字体: {font_name}', True, WHITE)
        screen.blit(font_info, (20, 170))

        pygame.display.update()
        clock.tick(GAME_SPEED)

if __name__ == '__main__':
    main() 
