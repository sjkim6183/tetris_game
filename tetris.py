import pygame
import random

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)

# 게임 보드 크기
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30

# 테트로미노 모양
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

SHAPE_COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = SHAPE_COLORS[SHAPES.index(self.shape)]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_WIDTH * BLOCK_SIZE, BOARD_HEIGHT * BLOCK_SIZE))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = [[BLACK for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False

    def new_piece(self):
        return Tetromino(BOARD_WIDTH // 2 - 1, 0)

    def valid_move(self, piece, dx, dy):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = piece.x + x + dx, piece.y + y + dy
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT or \
                       (new_y >= 0 and self.board[new_y][new_x] != BLACK):
                        return False
        return True

    def add_to_board(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[piece.y + y][piece.x + x] = piece.color

    def clear_lines(self):
        full_lines = [i for i, row in enumerate(self.board) if all(cell != BLACK for cell in row)]
        for line in full_lines:
            del self.board[line]
            self.board.insert(0, [BLACK for _ in range(BOARD_WIDTH)])

    def draw(self):
        self.screen.fill(BLACK)
        for y, row in enumerate(self.board):
            for x, color in enumerate(row):
                pygame.draw.rect(self.screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.current_piece.color,
                                     ((self.current_piece.x + x) * BLOCK_SIZE,
                                      (self.current_piece.y + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 0)

        pygame.display.flip()

    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.valid_move(self.current_piece, -1, 0):
                        self.current_piece.move(-1, 0)
                    if event.key == pygame.K_RIGHT and self.valid_move(self.current_piece, 1, 0):
                        self.current_piece.move(1, 0)
                    if event.key == pygame.K_DOWN and self.valid_move(self.current_piece, 0, 1):
                        self.current_piece.move(0, 1)
                    if event.key == pygame.K_UP:
                        rotated = Tetromino(self.current_piece.x, self.current_piece.y)
                        rotated.shape = list(zip(*self.current_piece.shape[::-1]))
                        if self.valid_move(rotated, 0, 0):
                            self.current_piece = rotated

            if self.valid_move(self.current_piece, 0, 1):
                self.current_piece.move(0, 1)
            else:
                self.add_to_board(self.current_piece)
                self.clear_lines()
                self.current_piece = self.new_piece()
                if not self.valid_move(self.current_piece, 0, 0):
                    self.game_over = True

            self.draw()
            self.clock.tick(5)

        pygame.quit()

if __name__ == "__main__":
    Tetris().run()