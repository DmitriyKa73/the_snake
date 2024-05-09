from random import choice, randint
import pygame as pg

# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self, body_color=SNAKE_COLOR) -> None:
        """Инициализация объекта игры."""
        self.body_color = body_color
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self) -> None:
        """Отрисовка объекта.
        Должен присутствовать в базовом классе в качестве затычки.
        """
        raise NotImplementedError(
            "Метод draw должен быть переопределен в дочерних классах."
        )

    def draw_cell(self, surface, position):
        """Метод отрисовки клетки объекта в игре."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        if self.body_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, body_color=APPLE_COLOR) -> None:
        """Инициализация объекта яблоко."""
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self) -> tuple:
        """Генерация случайной позиции для яблока."""
        return (
            randint(0, (GRID_WIDTH - 1)) * GRID_SIZE,
            randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE
        )

    def draw(self, surface) -> None:
        """Отрисовка яблока."""
        self.draw_cell(surface, self.position)

    def get_rect(self):
        """Получение квадрата, описывающего яблоко."""
        return pg.Rect(self.position[0], self.position[1],
                       GRID_SIZE, GRID_SIZE)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, body_color=SNAKE_COLOR) -> None:
        """Инициализация объекта змейка."""
        super().__init__(body_color)
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def update_direction(self, new_direction) -> None:
        """Обновление направления движения змейки."""
        self.direction = new_direction

    def move(self) -> None:
        """Метод, описывающий движение змейки."""
        self.head = [self.get_head_position()]
        directions = {
            RIGHT: (self.head[0][0] + GRID_SIZE, self.head[0][1]),
            LEFT: (self.head[0][0] - GRID_SIZE, self.head[0][1]),
            UP: (self.head[0][0], self.head[0][1] - GRID_SIZE),
            DOWN: (self.head[0][0], self.head[0][1] + GRID_SIZE)
        }
        self.new_position = directions[self.direction]
        x, y = self.new_position

        if x < 0:
            x = SCREEN_WIDTH - GRID_SIZE
        elif x >= SCREEN_WIDTH:
            x = 0
        if y < 0:
            y = SCREEN_HEIGHT - GRID_SIZE
        elif y >= SCREEN_HEIGHT:
            y = 0

        self.positions.insert(0, (x, y))
        self.last = self.positions[-1]
        if len(self.positions) > self.length:
            self.positions.pop(-1)

        if self.get_head_position() in self.positions[1:]:
            self.reset()

    def draw(self, surface) -> None:
        """Отрисовка змейки."""
        for position in self.positions[:-1]:
            self.draw_cell(surface, position)

        # Отрисовка головы змейки
        self.draw_cell(surface, self.positions[0])

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Получение позиции головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сброс состояния змейки."""
        self.length = 1
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object) -> None:
    """Обработка нажатий клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main() -> None:
    """Основная функция игры.
    Создает экземпляры классов для яблока и змейки, настраивает рабочий экран
    и управляет основным циклом игры.
    """
    apple = Apple(APPLE_COLOR)
    # apple.draw(screen)
    snake = Snake(SNAKE_COLOR)
    # snake.draw(screen)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction(snake.direction)
        snake.move()
        apple.draw(screen)
        snake.draw(screen)
        if snake.get_head_position() == (apple.position[0], apple.position[1]):
            snake.length += 1
            apple.position = apple.randomize_position()

        pg.display.update()


if __name__ == '__main__':
    """Этот блок кода запускает основную функцию игры."""
    main()
