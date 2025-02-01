import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

# Enhanced colors
WHITE = (240, 240, 240)  # Slightly off-white for better contrast
BLACK = (20, 20, 20)     # Soft black
# Snake colors for gradient effect
SNAKE_HEAD = (46, 139, 87)   # Sea green
SNAKE_BODY = (60, 179, 113)  # Medium sea green
SNAKE_TAIL = (84, 255, 159)  # Spring green
# Food and obstacle colors
FOOD_COLOR = (220, 20, 60)   # Crimson red
BOMB_COLOR = (255, 69, 0)    # Red-orange
BLOCK_COLOR = (105, 105, 105) # Dim gray
# Background grid color
GRID_COLOR = (230, 230, 230)  # Light gray for grid lines

# Initialize screen
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game using DSA")
except pygame.error as e:
    print(f"Failed to initialize display: {e}")
    sys.exit(1)

# Initialize fonts
try:
    font = pygame.font.Font(None, 30)
    large_font = pygame.font.Font(None, 50)
except pygame.error as e:
    print(f"Failed to initialize font: {e}")
    sys.exit(1)

def spawn_item():
    """Spawn items at random positions"""
    return [random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
            random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE]

def create_blocks():
    """Create fixed blocks in the middle of the field"""
    blocks = []
    # Create a few random blocks
    for _ in range(5):
        block = spawn_item()
        while block in blocks:
            block = spawn_item()
        blocks.append(block)
    return blocks

def show_game_over(score):
    """Show game over screen with retry option"""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    # Game Over text
    game_over_text = large_font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    retry_text = font.render("Press SPACE to retry or ESC to quit", True, WHITE)

    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(retry_text, (WIDTH//2 - retry_text.get_width()//2, HEIGHT//2 + 40))
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
    
def draw_grid():
    """Draw a subtle grid on the background"""
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_snake(snake):
    """Draw snake with gradient effect and rounded corners"""
    for i, segment in enumerate(snake):
        if i == 0:  # Head
            color = SNAKE_HEAD
        elif i == len(snake) - 1:  # Tail
            color = SNAKE_TAIL
        else:  # Body
            color = SNAKE_BODY
        
        # Draw rounded rectangle for each segment
        rect = pygame.Rect(*segment, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, rect, border_radius=CELL_SIZE//4)

def draw_food(pos):
    """Draw food with a glowing effect"""
    rect = pygame.Rect(*pos, CELL_SIZE, CELL_SIZE)
    # Draw main food circle
    pygame.draw.circle(screen, FOOD_COLOR, 
                      (pos[0] + CELL_SIZE//2, pos[1] + CELL_SIZE//2), 
                      CELL_SIZE//2)
    # Draw highlight
    pygame.draw.circle(screen, (255, 255, 255), 
                      (pos[0] + CELL_SIZE//3, pos[1] + CELL_SIZE//3), 
                      CELL_SIZE//6)

def draw_bomb(pos):
    """Draw bomb with warning effect"""
    rect = pygame.Rect(*pos, CELL_SIZE, CELL_SIZE)
    # Draw main bomb circle
    pygame.draw.circle(screen, BOMB_COLOR, 
                      (pos[0] + CELL_SIZE//2, pos[1] + CELL_SIZE//2), 
                      CELL_SIZE//2)
    # Draw warning pattern
    pygame.draw.line(screen, BLACK,
                    (pos[0] + CELL_SIZE//4, pos[1] + CELL_SIZE//4),
                    (pos[0] + 3*CELL_SIZE//4, pos[1] + 3*CELL_SIZE//4), 2)
    pygame.draw.line(screen, BLACK,
                    (pos[0] + 3*CELL_SIZE//4, pos[1] + CELL_SIZE//4),
                    (pos[0] + CELL_SIZE//4, pos[1] + 3*CELL_SIZE//4), 2)

def main():
    while True:  # Main game loop for restarts
        # Game Variables
        snake = [[100, 100]]
        direction = ["RIGHT"]
        food = spawn_item()
        blocks = create_blocks()
        bombs = [spawn_item()]  # Start with one bomb
        score = 0
        speed = 10
        running = True
        clock = pygame.time.Clock()

        while running:
            screen.fill(WHITE)
            draw_grid()  # Draw the background grid
            
            # Handle Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction[0] != "DOWN":
                        direction[0] = "UP"
                    elif event.key == pygame.K_DOWN and direction[0] != "UP":
                        direction[0] = "DOWN"
                    elif event.key == pygame.K_LEFT and direction[0] != "RIGHT":
                        direction[0] = "LEFT"
                    elif event.key == pygame.K_RIGHT and direction[0] != "LEFT":
                        direction[0] = "RIGHT"
            
            # Move the snake
            head = snake[0][:]
            if direction[0] == "UP":
                head[1] -= CELL_SIZE
            elif direction[0] == "DOWN":
                head[1] += CELL_SIZE
            elif direction[0] == "LEFT":
                head[0] -= CELL_SIZE
            elif direction[0] == "RIGHT":
                head[0] += CELL_SIZE

            # Wrap around screen
            head[0] = head[0] % WIDTH
            head[1] = head[1] % HEIGHT

            # Add the new head
            snake.insert(0, head)

            # Check for collisions
            game_over = False

            # Check collision with blocks
            if head in blocks:
                game_over = True

            # Check collision with bombs
            if head in bombs:
                game_over = True

            # Check collision with self
            if head in snake[1:]:
                game_over = True

            if game_over:
                if show_game_over(score):
                    break  # Break inner loop to restart
                return  # Exit game if not retrying

            # Check for food collision
            if head == food:
                score += 10
                food = spawn_item()
                # Spawn new bomb every 50 points
                if score % 50 == 0:
                    new_bomb = spawn_item()
                    while new_bomb in bombs or new_bomb in blocks:
                        new_bomb = spawn_item()
                    bombs.append(new_bomb)
            else:
                snake.pop()

            # Updated drawing code
            draw_snake(snake)
            draw_food(food)
            
            # Draw blocks with shadow effect
            for block in blocks:
                rect = pygame.Rect(*block, CELL_SIZE, CELL_SIZE)
                # Draw shadow
                shadow_rect = rect.copy()
                shadow_rect.move_ip(2, 2)
                pygame.draw.rect(screen, (50, 50, 50), shadow_rect)
                # Draw block
                pygame.draw.rect(screen, BLOCK_COLOR, rect)
            
            for bomb in bombs:
                draw_bomb(bomb)

            # Enhanced score display with shadow effect
            score_text = font.render(f"Score: {score}", True, BLACK)
            shadow_text = font.render(f"Score: {score}", True, (100, 100, 100))
            screen.blit(shadow_text, (12, 12))  # Shadow
            screen.blit(score_text, (10, 10))   # Main text

            pygame.display.update()
            clock.tick(speed)

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
        sys.exit()
