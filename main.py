import pygame
from lehmer32 import Lehmer
from starSystem import starSystem

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1024, 1024
GRID_SIZE = 50
FPS = 120
BACKGROUND_COLOR = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulating a universe")

# Clock to control frame rate
clock = pygame.time.Clock()

galaxyOffset = [0, 0]

starSelected = False
vStarSelected = [0, 0]
selectedStar = None
def draw():
    global starSelected, vStarSelected, selectedStar # Declare them as global

    keys = pygame.key.get_pressed()
    speed = 100  # Movement speed in pixels per second
    elapsedTime = clock.get_time() / 24  # Convert to seconds

    # Move galaxy offset
    if keys[pygame.K_LEFT]:
        galaxyOffset[0] -= speed * elapsedTime
    if keys[pygame.K_RIGHT]:
        galaxyOffset[0] += speed * elapsedTime
    if keys[pygame.K_UP]:
        galaxyOffset[1] -= speed * elapsedTime
    if keys[pygame.K_DOWN]:
        galaxyOffset[1] += speed * elapsedTime

    # Get mouse position in grid
    mouse_pos = pygame.mouse.get_pos()
    mouse_world_x = (mouse_pos[0] + galaxyOffset[0]) // GRID_SIZE
    mouse_world_y = (mouse_pos[1] + galaxyOffset[1]) // GRID_SIZE
    mouse_grid = [mouse_world_x, mouse_world_y]

    mouse = pygame.mouse.get_pressed()

    screen.fill(BACKGROUND_COLOR)

    nSectorX = WIDTH // GRID_SIZE
    nSectorY = HEIGHT // GRID_SIZE

    for x in range(nSectorX):
        for y in range(nSectorY):
            world_x = x + galaxyOffset[0] // GRID_SIZE
            world_y = y + galaxyOffset[1] // GRID_SIZE

            star = starSystem(world_x, world_y)
            if star.starExists:
                # Convert world coordinates back to screen space
                screen_x = x * GRID_SIZE
                screen_y = y * GRID_SIZE

                pygame.draw.circle(screen, star.starColor, (screen_x, screen_y), star.starDiameter)

                # If mouse is over this star, draw a border
                if mouse_grid == [world_x, world_y]:
                    pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), star.starDiameter + 3, 2)

                    # If left-click is pressed, select the star
                    if mouse[0]:
                        selectedStar = starSystem(world_x, world_y, generateFullSystem=True)  
                        starSelected = True
                        vStarSelected = [world_x, world_y]

                        print(f"Star selected at: {vStarSelected}")
    if starSelected and selectedStar:
        draw_star_info(selectedStar)

# TODO: Chnage this shit:
def draw_star_info(selectedStar):
    """ Draws the planet and moon details in a panel. """
    panel_width, panel_height = 300, 400
    panel_x, panel_y = WIDTH - panel_width - 20, 20

    panel = pygame.Surface((panel_width, panel_height))
    panel.fill((50, 50, 50))

    font = pygame.font.Font(None, 24)
    title_text = font.render(f"Star System", True, (255, 255, 255))
    panel.blit(title_text, (10, 10))

    y_offset = 40
    for i, planet in enumerate(selectedStar.planets):
        planet_text = font.render(f"Planet {i+1} - Size: {planet.diameter:.1f}", True, (200, 200, 200))
        panel.blit(planet_text, (10, y_offset))
        y_offset += 25

        moon_text = font.render(f" Moons: {planet.moons}", True, (180, 180, 180))
        panel.blit(moon_text, (20, y_offset))
        y_offset += 20

    screen.blit(panel, (panel_x, panel_y))


    # Draw selected star highlight
    if starSelected:
        selected_screen_x = (vStarSelected[0] - galaxyOffset[0] // GRID_SIZE) * GRID_SIZE
        selected_screen_y = (vStarSelected[1] - galaxyOffset[1] // GRID_SIZE) * GRID_SIZE
        pygame.draw.circle(screen, (255, 255, 0), (selected_screen_x, selected_screen_y), 5)  # Small highlight

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
