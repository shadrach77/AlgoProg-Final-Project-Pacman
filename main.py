import pygame
import sys
import random
import math

pygame.init()

# Colors
BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW=(255,255,0)
WHITE=(255,255,255)
RED=(255,0,0)
PINK=(255,192,203)
CYAN=(0,255,255)
ORANGE=(255,105,0)

# Screen Dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
CELL_SIZE = 40

# Grid Dimenstions
GRID_WIDTH = 15
GRID_HEIGHT = 15

# Game States
PLAYING = 0
GAME_OVER = 1
WIN = 2

# Global Game State
game_state = PLAYING

# Create Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

#Font for Score
font = pygame.font.Font(None, 36)

# Game Grid
grid = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,0,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Pac Man
class PacMan:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 3  # 0:right, 1:down, 2:left, 3:up
        self.mouth_open = False

    def move(self, grid):
        dx, dy = [(1,0), (0,1), (-1,0), (0,-1)][self.direction]
        new_x = self.x + dx
        new_y = self.y + dy

        if grid[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

            if grid[new_y][new_x] == 0:
                grid[new_y][new_x] = 2
                return True  # pellet eaten
        return False

    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 50

        mouth_opening = 45 if self.mouth_open else 0
        pygame.draw.circle(screen, YELLOW, (x, y), CELL_SIZE // 2)

        if self.direction == 0:
            start_angle, end_angle = 360 - mouth_opening/2, mouth_opening/2
        elif self.direction == 1:
            start_angle, end_angle = 270 - mouth_opening/2, 270 + mouth_opening/2
        elif self.direction == 2:
            start_angle, end_angle = 180 - mouth_opening/2, 180 + mouth_opening/2
        else:
            start_angle, end_angle = 90 - mouth_opening/2, 90 + mouth_opening/2

        pygame.draw.arc(
            screen,
            BLACK,
            (x - CELL_SIZE//2, y - CELL_SIZE//2, CELL_SIZE, CELL_SIZE),
            math.radians(start_angle),
            math.radians(end_angle),
            CELL_SIZE // 2
        )

pacman = PacMan(1, 1)

# Ghosts
class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, grid):
        directions = [(1,0), (0,1), (-1,0), (0,-1)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy

            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                if grid[new_y][new_x] != 1:
                    self.x = new_x
                    self.y = new_y
                    break

    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 50
        pygame.draw.circle(screen, self.color, (x, y), CELL_SIZE // 2)

ghosts = [
    Ghost(1, 13, RED),
    Ghost(13, 1, PINK),
    Ghost(13, 13, CYAN),
    Ghost(11, 11, ORANGE)
]

# Score
score = 0

# Game Loop
clock = pygame.time.Clock()
running = True

# Movement delays
pacman_move_delay = 150  # milliseconds
ghost_move_delay = 300
mouth_anim_delay = 600

#timing varibles
last_pacman_move_time = 0
last_ghost_move_time = 0
last_mouth_anim_time = 0

def reset_game():
    global pacman, ghosts, score, grid, game_state
    pacman = PacMan(1, 1)
    ghosts = [
    Ghost(1, 13, RED),
    Ghost(13, 1, PINK),
    Ghost(13, 13, CYAN),
    Ghost(11, 11, ORANGE)
]
    score = 0
    grid = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
        [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
        [1,1,1,1,0,1,0,0,0,1,0,1,1,1,1],
        [1,1,1,1,0,1,0,1,0,1,0,1,1,1,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,1,1,1,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]
    game_state = PLAYING

def draw_win_screen():
    screen.fill(BLACK)
    win_font = pygame.font.Font(None, 64)
    score_font = pygame.font.Font(None, 48)
    restart_font = pygame.font.Font(None, 36)

    win_text = win_font.render("YOU WIN!", True, YELLOW)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    restart_text = restart_font.render("Press SPACE to restart", True, CYAN)

    screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 2 * SCREEN_HEIGHT // 3))

def draw_game_over():
    screen.fill(BLACK)
    game_over_font = pygame.font.Font(None, 64)
    score_font = pygame.font.Font(None, 48)
    restart_font = pygame.font.Font(None, 36)

    game_over_text = game_over_font.render("GAME OVER", True, RED)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    restart_text = restart_font.render("Press SPACE to restart", True, YELLOW)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 2 * SCREEN_HEIGHT // 3))

#Main game loop
running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_state == PLAYING:
                if event.key == pygame.K_UP:
                    pacman.direction =  3
                elif event.key == pygame.K_DOWN:
                    pacman.direction = 1
                elif event.key == pygame.K_LEFT:
                    pacman.direction =2
                elif event.key == pygame.K_RIGHT:
                    pacman.direction = 0
            elif game_state == GAME_OVER:
                if event.key == pygame.K_SPACE:
                    reset_game()
            elif game_state in (GAME_OVER, WIN):
                if event.key == pygame.K_SPACE:
                    reset_game()

    if game_state == PLAYING:
        # Move pacman only if enough time has passed
        if current_time - last_pacman_move_time > pacman_move_delay:
            if pacman.move(grid):
                # Check win condition
                if not any(0 in row for row in grid):
                    game_state = WIN
                score += 10
            last_pacman_move_time = current_time    
        # Move ghosts only if enough time has passed
        if current_time - last_ghost_move_time > ghost_move_delay:
            for ghost in ghosts:
                ghost.move(grid)
            last_ghost_move_time = current_time
        # Animate pacman's mouth
        if current_time - last_mouth_anim_time > mouth_anim_delay:
            pacman.mouth_open = not pacman.mouth_open
            last_mouth_anim_time = current_time


        # clear the screen
        screen.fill(BLACK)
        # Draw the maze and dots
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x] == 1:
                    pygame.draw.rect(screen, BLUE, (x*CELL_SIZE, y*CELL_SIZE+50, CELL_SIZE, CELL_SIZE))
                elif grid[y][x] == 0:
                    pygame.draw.circle(screen, YELLOW, (x*CELL_SIZE+CELL_SIZE//2, y*CELL_SIZE+CELL_SIZE//2+50), 3)
                    
        #Draw pacman     
        pacman.draw(screen)
        #Draw ghost
        for ghost in ghosts:
            ghost.draw(screen)
        #displaying the socre
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text,(10,10))

        # Screen instruction
        instructions = font.render("Arrow Keys: Move | ESC: Quit", True, WHITE)
        screen.blit(instructions, (200, 10))

        # Check for collision with ghosts
        for ghost in ghosts:
            if pacman.x == ghost.x and pacman.y == ghost.y:
                game_state = GAME_OVER

    elif game_state == GAME_OVER:
        draw_game_over()
    elif game_state == WIN:
        draw_win_screen()    

    # update the display
    pygame.display.flip()

    #cap the fram rate
    clock.tick(60)

pygame.quit()

sys.exit()
