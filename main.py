import pygame
from lehmer32 import Lehmer
import math
from starSystem import starSystem
# from main import starSelected

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 1000
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
    panel_width, panel_height = 1000, 500
    panel_x, panel_y = 0, 500 

    panel = pygame.Surface((panel_width, panel_height))
    panel.fill((50, 50, 50))

    font = pygame.font.Font(None, 24)
    star_x = int((selectedStar.starDiameter * 3 / 2) + 100)
    star_y = panel_height // 2
    pygame.draw.circle(panel, selectedStar.starColor, (star_x, star_y), selectedStar.starDiameter * 3)
    
    title_text = font.render("Star System", True, (255, 255, 255))
    panel.blit(title_text, (10, 10))

    # Draw planets and their moons
    max_distance = max((p.distance for p in selectedStar.planets), default=1)  # Avoid division by zero
    start_x = star_x + selectedStar.starDiameter  # Start drawing planets after the star

    for planet in selectedStar.planets:

        spacing = (panel_width - start_x - 50) // max(1, len(selectedStar.planets))  # Avoid division by zero
        for i, planet in enumerate(selectedStar.planets):
            planet_x = start_x + i * spacing 
        planet_y = star_y
        
        # Draw the planet
        print(f"Planet {planet.distance}: diameter={planet.diameter}, size={max(5, int(round(planet.diameter * 2)))}")

        planet_size = max(5, int(round(planet.diameter * 2)))  # Always an integer

        pygame.draw.circle(panel, (0, 255, 0), (planet_x, planet_y), planet_size)  # Green for planets
        
        # Draw moons
        moon_angle_step = 360 // max(planet.moons, 1)  # Distribute moons in a circle
        moon_distance = planet_size + 8  # Offset from planet
        
        for m in range(planet.moons):
            angle = m * moon_angle_step
            moon_x = planet_x + int(moon_distance * math.cos(math.radians(angle)))
            moon_y = planet_y + int(moon_distance * math.sin(math.radians(angle)))
            moon_y = planet_y + int(moon_distance * math.sin(math.radians(angle)))
            pygame.draw.circle(panel, (200, 200, 200), (moon_x, moon_y), 3)  # Gray for moons
        
        # Label planets
        planet_text = font.render(f"P{planet.distance:.1f}", True, (255, 255, 255))
        panel.blit(planet_text, (planet_x - 10, planet_y + planet_size + 5))

    # Blit panel to screen
    screen.blit(panel, (panel_x, panel_y))
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
