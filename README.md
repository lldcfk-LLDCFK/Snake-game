# Snake Game with AI Opponent 🐍

A modern implementation of the classic Snake game using Python and Pygame, featuring an AI opponent and multiple food items.

## Features ✨

- Classic snake gameplay with smooth controls
- AI opponent that competes for food
- Multiple food items with different colors
- Score tracking for both player and AI
- Custom font support with font switching capability
- Responsive window design
- Collision detection and game reset functionality

## Requirements 📋

- Python 3.x
- Pygame

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/yourusername/snake-game.git
cd snake-game
```

2. Install the required dependencies:
```bash
# Using requirements.txt (recommended)
pip install -r requirements.txt

# Or install pygame directly
pip install pygame
```

## How to Play 🎮

1. Run the game:
```bash
python snake_game.py
```

2. Controls:
- Use arrow keys to control the snake's direction
- Press 'F' to switch between available fonts
- Close the window to exit the game

## Game Rules 📜

- The snake grows when it eats food
- The game resets if the snake collides with itself
- Both player and AI compete for the same food items
- The snake can pass through walls and appear on the opposite side

## Customization 🎨

You can customize the game by modifying these parameters in the code:
- `WINDOW_WIDTH` and `WINDOW_HEIGHT`: Change the window size
- `BLOCK_SIZE`: Adjust the size of the snake and food
- `GAME_SPEED`: Modify the game speed
- `FOOD_COUNT`: Change the number of food items

## Font Support 🖋️

The game supports custom fonts. Place your font files in the `gameFONTS` directory:
- Supported formats: .ttf, .ttc
- Default font will be used if no custom fonts are found

---

# 贪吃蛇游戏与AI对手 🐍

使用Python和Pygame实现的现代版经典贪吃蛇游戏，具有AI对手和多种食物特性。

## 特性 ✨

- 流畅控制的经典贪吃蛇玩法
- 竞争食物的AI对手
- 多种颜色的食物
- 玩家和AI的分数追踪
- 自定义字体支持，可切换字体
- 响应式窗口设计
- 碰撞检测和游戏重置功能

## 系统要求 📋

- Python 3.x
- Pygame

## 安装说明 🚀

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/snake-game.git
cd snake-game
```

2. 安装所需依赖：
```bash
# 使用 requirements.txt 安装（推荐）
pip install -r requirements.txt

# 或直接安装 pygame
pip install pygame
```

## 游戏玩法 🎮

1. 运行游戏：
```bash
python snake_game.py
```

2. 控制方式：
- 使用方向键控制蛇的移动方向
- 按'F'键切换可用字体
- 关闭窗口退出游戏

## 游戏规则 📜

- 蛇吃到食物后会变长
- 蛇撞到自己时游戏重置
- 玩家和AI竞争相同的食物
- 蛇可以穿过墙壁从对面出现

## 自定义设置 🎨

你可以通过修改代码中的以下参数来自定义游戏：
- `WINDOW_WIDTH` 和 `WINDOW_HEIGHT`：更改窗口大小
- `BLOCK_SIZE`：调整蛇和食物的大小
- `GAME_SPEED`：修改游戏速度
- `FOOD_COUNT`：更改食物数量

## 字体支持 🖋️

游戏支持自定义字体。将字体文件放在 `gameFONTS` 目录中：
- 支持的格式：.ttf, .ttc
- 如果未找到自定义字体，将使用默认字体

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
