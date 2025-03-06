import pygame
from lehmer32 import Lehmer
from starSystem import starSystem


# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 1000
FPS = 60  # Frames per second
BACKGROUND_COLOR = (0, 0, 0)  # Dark blue background

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulating a universe")

# Clock to control frame rate
clock = pygame.time.Clock()

galaxyOffset = [0, 0]

def draw():
    keys = pygame.key.get_pressed()
    speed = 1

    elapsedTime = clock.get_time() / 100

    if(keys[pygame.K_LEFT]):
       galaxyOffset[0] -= speed * elapsedTime
    if(keys[pygame.K_RIGHT]):
       galaxyOffset[0] += speed * elapsedTime
    if(keys[pygame.K_UP]):
       galaxyOffset[1] -= speed * elapsedTime
    if(keys[pygame.K_DOWN]):
       galaxyOffset[1] += speed * elapsedTime


    screen.fill(BACKGROUND_COLOR)

    nSectorX = WIDTH // 16
    nSectorY = HEIGHT // 16

    for x in range(nSectorX):
        for y in range(nSectorY):
                print("checking in ", x, " ", y)
                star = starSystem(x + galaxyOffset[0], y + galaxyOffset[1])
                if(star.starExists):
                    print("star exists at", x, " ", y)
                    pygame.draw.circle(screen, star.starColor, (x * 50, y * 50), star.starDiameter)
# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close the game
            running = False

    # Game logic (update objects here)
    # # Drawing
    # screen.fill(BACKGROUND_COLOR)  # Clear the screen
    # # pygame.draw.circle(screen, (255, 255, 0), (WIDTH // 2, HEIGHT // 2), 50)  # Example: Draw a yellow circle

    draw()

    # Refresh screen
    pygame.display.flip()

    # Maintain frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
