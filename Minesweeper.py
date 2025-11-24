import pygame, random, sys, time

# Initialize Pygame
pygame.init()
pygame.font.init()

# ---------------- SETTINGS ----------------
ROWS, COLS = 16, 16
MINES = 35
CELL = 35
HEADER = 60
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + HEADER

# Colors (Google Minesweeper style)
COLOR_HIDDEN = [(170, 215, 81), (162, 209, 73)]
COLOR_REVEALED = [(229, 194, 159), (215, 184, 153)]
COLOR_HEADER = (110, 150, 50)
COLOR_FLAG = (255, 0, 0)
COLOR_MINE = (40, 40, 40)

# Number colors
NUM_COLORS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128)
}

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
font = pygame.font.SysFont("arial", 22, bold=True)
clock = pygame.time.Clock()

# ---------------- GAME STATE ----------------
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]

# Directions for neighbors
dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

# Place mines
mines = set()
while len(mines) < MINES:
    r, c = random.randint(0, ROWS-1), random.randint(0, COLS-1)
    mines.add((r, c))

# Calculate numbers
for r in range(ROWS):
    for c in range(COLS):
        if (r, c) in mines:
            board[r][c] = -1
        else:
            board[r][c] = sum((r+dr, c+dc) in mines for dr, dc in dirs)

# ---------------- FUNCTIONS ----------------
def draw_header(flags_left, elapsed):
    pygame.draw.rect(screen, COLOR_HEADER, (0, 0, WIDTH, HEADER))
    text_flags = font.render(f"🚩 {flags_left}", True, (255, 255, 255))
    text_time = font.render(f"⏱️ {elapsed:03d}", True, (255, 255, 255))
    screen.blit(text_flags, (20, 15))
    screen.blit(text_time, (WIDTH - 120, 15))

def draw_board():
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL, r * CELL + HEADER
            rect = pygame.Rect(x, y, CELL, CELL)
            base_color = COLOR_HIDDEN[(r + c) % 2]

            if revealed[r][c]:
                color = COLOR_REVEALED[(r + c) % 2]
                pygame.draw.rect(screen, color, rect, border_radius=4)
                if board[r][c] > 0:
                    num_color = NUM_COLORS.get(board[r][c], (0, 0, 0))
                    text = font.render(str(board[r][c]), True, num_color)
                    screen.blit(text, (x + 12, y + 6))
                elif board[r][c] == -1:
                    pygame.draw.circle(screen, COLOR_MINE, rect.center, 10)
            elif flagged[r][c]:
                pygame.draw.rect(screen, base_color, rect, border_radius=4)
                pygame.draw.polygon(screen, COLOR_FLAG, [
                    (x + 10, y + 25),
                    (x + 25, y + 15),
                    (x + 10, y + 5)
                ])
            else:
                pygame.draw.rect(screen, base_color, rect, border_radius=4)

def reveal_cell(r, c):
    if revealed[r][c] or flagged[r][c]:
        return
    revealed[r][c] = True
    if board[r][c] == 0:
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                reveal_cell(nr, nc)

def check_win():
    for r in range(ROWS):
        for c in range(COLS):
            if not revealed[r][c] and (r, c) not in mines:
                return False
    return True

# ---------------- MAIN LOOP ----------------
running = True
game_over = False
win = False
start_time = time.time()
flags_left = MINES

while running:
    screen.fill((0, 0, 0))
    elapsed = int(time.time() - start_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if my > HEADER:
                    r, c = (my - HEADER) // CELL, mx // CELL
                    if event.button == 1:  # Left click
                        if not flagged[r][c]:
                            if (r, c) in mines:
                                revealed[r][c] = True
                                game_over = True
                            else:
                                reveal_cell(r, c)
                                win = check_win()
                    elif event.button == 3:  # Right click
                        if not revealed[r][c]:
                            flagged[r][c] = not flagged[r][c]
                            flags_left += -1 if flagged[r][c] else 1

    # Draw header and board
    draw_header(flags_left, elapsed)
    draw_board()

    if game_over:
        text = font.render("💥 Game Over!", True, (255, 50, 50))
        screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    elif win:
        text = font.render("🎉 You Win!", True, (0, 200, 0))
        screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2 - 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
