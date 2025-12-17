import pygame
import random
import sys
import time
import array 

# Initialize Pygame and Mixer (Audio)
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.font.init()

# ---------------- SETTINGS ----------------
ROWS, COLS = 16, 16
MINES = 30
CELL = 35
HEADER = 80
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + HEADER

# COLORS
COLOR_HIDDEN = [(45, 45, 50), (50, 50, 55)]
COLOR_REVEALED = [(20, 20, 20), (25, 25, 25)]
COLOR_HEADER = (10, 10, 10)
COLOR_FLAG = (255, 69, 0)
COLOR_MINE = (200, 0, 0)
COLOR_TEXT_TIME = (255, 50, 50)
COLOR_BTN_PLAY = (0, 150, 0)
COLOR_BTN_EXIT = (150, 0, 0)
COLOR_BTN_TEXT = (255, 255, 255)

# Neon Number colors
NUM_COLORS = {
    1: (66, 135, 245), 2: (50, 205, 50), 3: (255, 50, 50),
    4: (147, 112, 219), 5: (255, 165, 0), 6: (0, 255, 255),
    7: (255, 255, 255), 8: (128, 128, 128)
}

# setup 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MINESWEEPER")
font = pygame.font.SysFont("consolas", 30, bold=True)
big_font = pygame.font.SysFont("consolas", 40, bold=True)
small_font = pygame.font.SysFont("consolas", 25)
clock = pygame.time.Clock()

# ---------------- AUDIO GENERATION ----------------
def generate_explosion_sound():
    """Generates a synthetic 'white noise' explosion sound."""
    duration = 2  # seconds
    frequency = 22050
    num_samples = int(duration * frequency)
    
    sound_buffer = array.array('h', [0] * num_samples)
    
    for i in range(num_samples):
        volume = 32767 * (1.0 - (i / num_samples))
        sound_buffer[i] = int(random.uniform(-volume, volume))
        
    return pygame.mixer.Sound(buffer=sound_buffer)

# Create the sound object
try:
    EXPLOSION_SFX = generate_explosion_sound()
    EXPLOSION_SFX.set_volume(0.5)
except Exception as e:
    print(f"Audio Warning: Could not generate sound. {e}")
    EXPLOSION_SFX = None

# ---------------- GAME VARIABLES ----------------

dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# Button Rectangles (Initialized as placeholders, updated in draw loop)
btn_play_rect = pygame.Rect(0, 0, 0, 0)
btn_exit_rect = pygame.Rect(0, 0, 0, 0)

# ---------------- LOGIC ----------------

def reset_game():
    global board, revealed, flagged, mines, first_click_done, game_over, win, start_time, flags_left, shake_duration
    
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    mines = set()
    first_click_done = False
    game_over = False
    win = False
    start_time = None
    flags_left = MINES
    shake_duration = 0

def generate_mines(exclude_r, exclude_c):
    safe_zone = set()
    safe_zone.add((exclude_r, exclude_c))
    for dr, dc in dirs:
        safe_zone.add((exclude_r + dr, exclude_c + dc))

    while len(mines) < MINES:
        r, c = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        if (r, c) not in safe_zone:
            mines.add((r, c))

    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) in mines:
                board[r][c] = -1
            else:
                board[r][c] = sum((r + dr, c + dc) in mines for dr, dc in dirs)

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

def trigger_chain_reaction():
    global shake_duration
    shake_duration = 60
    
    if EXPLOSION_SFX:
        EXPLOSION_SFX.play()

    for (r, c) in mines:
        revealed[r][c] = True

def draw_header(flags_left, time_elapsed):
    pygame.draw.rect(screen, COLOR_HEADER, (0, 0, WIDTH, HEADER))
    text_flags = font.render(f"FLAGS: {flags_left}", True, (200, 200, 200))
    screen.blit(text_flags, (20, 25))
    
    color = (255, 255, 255)
    text_time = big_font.render(f"{time_elapsed:03d}", True, color)
    screen.blit(text_time, (WIDTH // 1.2 - 50, 15))

def draw_board(shake_offset_x, shake_offset_y):
    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL + shake_offset_x
            y = r * CELL + HEADER + shake_offset_y
            rect = pygame.Rect(x, y, CELL, CELL)
            base_color = COLOR_HIDDEN[(r + c) % 2]

            if revealed[r][c]:
                if board[r][c] == -1:
                    pygame.draw.rect(screen, (50, 0, 0), rect)
                    if game_over and not win:
                        flicker = random.randint(-2, 2)
                        radius = (int(time.time() * 20) % 15) + 5 + flicker
                        pygame.draw.circle(screen, (255, 50, 0), rect.center, radius)
                        pygame.draw.circle(screen, (255, 255, 0), rect.center, radius - 4)
                    else:
                        pygame.draw.circle(screen, (0, 0, 0), rect.center, 10)
                else:
                    color = COLOR_REVEALED[(r + c) % 2]
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (30,30,30), rect, 1)
                    if board[r][c] > 0:
                        num_color = NUM_COLORS.get(board[r][c], (255, 255, 255))
                        text = font.render(str(board[r][c]), True, num_color)
                        screen.blit(text, (x + 12, y + 6))

            elif flagged[r][c]:
                pygame.draw.rect(screen, base_color, rect)
                pygame.draw.polygon(screen, COLOR_FLAG, [
                    (x + 10, y + 25), (x + 25, y + 15), (x + 10, y + 5)
                ])
            else:
                pygame.draw.rect(screen, base_color, rect)

def draw_end_buttons():
    global btn_play_rect, btn_exit_rect
    
    # Button Dimensions
    btn_w, btn_h = 200, 60
    center_x = WIDTH // 2
    
    # Define Rects
    btn_play_rect = pygame.Rect(center_x - btn_w - 10, HEIGHT // 2 + 50, btn_w, btn_h)
    btn_exit_rect = pygame.Rect(center_x + 10, HEIGHT // 2 + 50, btn_w, btn_h)
    
    # Draw Play Button
    pygame.draw.rect(screen, COLOR_BTN_PLAY, btn_play_rect, border_radius=10)
    pygame.draw.rect(screen, (255,255,255), btn_play_rect, 2, border_radius=10)
    text_play = font.render("PLAY AGAIN", True, COLOR_BTN_TEXT)
    screen.blit(text_play, (btn_play_rect.centerx - text_play.get_width()//2, btn_play_rect.centery - text_play.get_height()//2))

    # Draw Exit Button
    pygame.draw.rect(screen, COLOR_BTN_EXIT, btn_exit_rect, border_radius=10)
    pygame.draw.rect(screen, (255,255,255), btn_exit_rect, 2, border_radius=10)
    text_exit = font.render("EXIT", True, COLOR_BTN_TEXT)
    screen.blit(text_exit, (btn_exit_rect.centerx - text_exit.get_width()//2, btn_exit_rect.centery - text_exit.get_height()//2))

# ---------------- MAIN LOOP ----------------
reset_game()
running = True

while running:
    # 1. UPDATE
    if not game_over and not win:
        if start_time is None:
            time_elapsed = 0
        else:
            time_elapsed = int(time.time() - start_time)
            
    # 2. INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            
            # --- GAME ACTIVE LOGIC ---
            if not game_over and not win:
                if my > HEADER:
                    r, c = (my - HEADER) // CELL, mx // CELL
                    
                    if event.button == 1:  # Left click
                        if not flagged[r][c]:
                            if not first_click_done:
                                generate_mines(r, c)
                                first_click_done = True
                                start_time = time.time() 

                            if (r, c) in mines:
                                game_over = True
                                trigger_chain_reaction()
                            else:
                                reveal_cell(r, c)
                                win = check_win()
                                
                    elif event.button == 3:  # Right click
                        if not revealed[r][c]:
                            flagged[r][c] = not flagged[r][c]
                            flags_left += -1 if flagged[r][c] else 1
            
            # --- GAME OVER / WIN LOGIC ---
            else:
                if event.button == 1: # Left Click Only
                    if btn_play_rect.collidepoint((mx, my)):
                        reset_game()
                    elif btn_exit_rect.collidepoint((mx, my)):
                        running = False

    # 3. DRAW
    sx, sy = 0, 0
    if shake_duration > 0:
        shake_duration -= 1
        magnitude = shake_duration // 3
        sx = random.randint(-magnitude, magnitude)
        sy = random.randint(-magnitude, magnitude)

    draw_header(flags_left, time_elapsed)
    draw_board(sx, sy)

    if game_over:
        if not win:
            text = big_font.render("TOTAL FAILURE", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - 130, HEIGHT // 2 - 50))    
            draw_end_buttons() # Draw buttons on top
    elif win:
        text = big_font.render("MISSION ACCOMPLISHED", True, (0, 255, 0))
        screen.blit(text, (WIDTH // 2 - 180, HEIGHT // 2 - 50))
        draw_end_buttons() # Draw buttons on top

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

sys.exit()

