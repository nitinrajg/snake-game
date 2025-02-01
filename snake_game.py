import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants (these can stay outside)
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialize screen
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game with Power-ups")
except pygame.error as e:
    print(f"Failed to initialize display: {e}")
    sys.exit(1)

# Initialize font
try:
    font = pygame.font.Font(None, 30)
except pygame.error as e:
    print(f"Failed to initialize font: {e}")
    sys.exit(1)

def spawn_power_up():
    """
    Randomly generates power-ups on the screen.
    20% chance to spawn a power-up when called.
    """
    if random.randint(1, 5) == 1:  # 20% chance
        return [random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE]
    return None

def main():
    # Game Variables (moved inside main)
    snake = [[100, 100]]
    direction = ["RIGHT"]
    food = [random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
            random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE]
    power_up = None
    power_up_timer = 0
    score = 0
    speed = 10
    running = True
    clock = pygame.time.Clock()

    while running:
        # Fill the screen with white color
        screen.fill(WHITE)
        
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction[0] != "DOWN":
                    direction[0] = "UP"
                elif event.key == pygame.K_DOWN and direction[0] != "UP":
                    direction[0] = "DOWN"
                elif event.key == pygame.K_LEFT and direction[0] != "RIGHT":
                    direction[0] = "LEFT"
                elif event.key == pygame.K_RIGHT and direction[0] != "LEFT":
                    direction[0] = "RIGHT"
        
        # Move the snake: Create a new head based on the current direction
        head = snake[0][:]  # Copy the current head
        if direction[0] == "UP":
            head[1] -= CELL_SIZE
        elif direction[0] == "DOWN":
            head[1] += CELL_SIZE
        elif direction[0] == "LEFT":
            head[0] -= CELL_SIZE
        elif direction[0] == "RIGHT":
            head[0] += CELL_SIZE

        # Add the new head to the snake
        snake.insert(0, head)

        # Check for collision with food
        if head == food:
            score += 10
            food = [random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                    random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE]
            # Try spawning a power-up if one isn't already present
            if not power_up:
                power_up = spawn_power_up()
        else:
            # Remove the tail segment if no food is eaten to simulate movement
            snake.pop()

        # Check for collision with self or walls (game over condition)
        if (head in snake[1:] or
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT):
            running = False  # End the game
        
        # Check for collision with power-up
        if power_up and head == power_up:
            power_up_timer = 100  # Activate power-up effect for a limited number of frames
            speed = 15           # Increase speed temporarily
            score += 20          # Award bonus points
            power_up = None      # Remove the power-up from the board

        # Handle power-up effect duration: reset speed when timer expires
        if power_up_timer > 0:
            power_up_timer -= 1
        else:
            speed = 10  # Reset to normal speed

        # Draw the snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

        # Draw the food
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))

        # Draw the power-up, if available
        if power_up:
            pygame.draw.rect(screen, BLUE, (*power_up, CELL_SIZE, CELL_SIZE))

        # Display the score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the display and tick the clock
        pygame.display.update()
        clock.tick(speed)

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
        sys.exit()
