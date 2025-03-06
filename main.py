import pygame
from lehmer32 import Lehmer
import math
from starSystem import Planet, starSystem

pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 1000
GRID_SIZE = 50
FPS = 120
BACKGROUND_COLOR = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulating a universe")

clock = pygame.time.Clock()

galaxyOffset = [0, 0]
starSelected = False
vStarSelected = [0, 0]
selectedStar = None
hoveredPlanet = None

def draw():
    global starSelected, vStarSelected, selectedStar, hoveredPlanet

    keys = pygame.key.get_pressed()
    speed = 100  
    elapsedTime = clock.get_time() / 24  

    # Move galaxy offset
    if keys[pygame.K_LEFT]:
        galaxyOffset[0] -= speed * elapsedTime
    if keys[pygame.K_RIGHT]:
        galaxyOffset[0] += speed * elapsedTime
    if keys[pygame.K_UP]:
        galaxyOffset[1] -= speed * elapsedTime
    if keys[pygame.K_DOWN]:
        galaxyOffset[1] += speed * elapsedTime

    mouse_pos = pygame.mouse.get_pos()
    mouse_world_x = (mouse_pos[0] + galaxyOffset[0]) // GRID_SIZE
    mouse_world_y = (mouse_pos[1] + galaxyOffset[1]) // GRID_SIZE
    mouse_grid = [mouse_world_x, mouse_world_y]

    mouse = pygame.mouse.get_pressed()

    screen.fill(BACKGROUND_COLOR)

    nSectorX = WIDTH // GRID_SIZE
    nSectorY = HEIGHT // GRID_SIZE

    panel_rect = pygame.Rect(0, 500, WIDTH, 500)  

    clicked_outside = mouse[0] and not panel_rect.collidepoint(mouse_pos)  

    starClicked = False  

    for x in range(nSectorX):
        for y in range(nSectorY):
            world_x = x + galaxyOffset[0] // GRID_SIZE
            world_y = y + galaxyOffset[1] // GRID_SIZE

            star = starSystem(world_x, world_y)
            if star.starExists:
                screen_x = x * GRID_SIZE
                screen_y = y * GRID_SIZE

                pygame.draw.circle(screen, star.starColor, (screen_x, screen_y), star.starDiameter)

                if mouse_grid == [world_x, world_y]:  
                    pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), star.starDiameter + 3, 2)

                    if mouse[0]:  
                        selectedStar = starSystem(world_x, world_y, generateFullSystem=True)  
                        starSelected = True
                        vStarSelected = [world_x, world_y]
                        starClicked = True  
                        print(f"Star selected at: {vStarSelected}")

    if clicked_outside and not starClicked:
        starSelected = False  

    if starSelected:
        draw_star_info(selectedStar)

def draw_star_info(selectedStar):
    global hoveredPlanet

    if not selectedStar:
        return

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

    # **Star Details**
    star_details = [
        f"Name: {selectedStar.name}",
        f"Type: {selectedStar.type}",
        f"Size: {selectedStar.starDiameter} units",
        f"Planets: {len(selectedStar.planets)}"
    ]

    y_offset = 40
    for line in star_details:
        detail_render = font.render(line, True, (255, 255, 255))
        panel.blit(detail_render, (10, y_offset))
        y_offset += 20

    # Get mouse position relative to panel
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x -= panel_x
    mouse_y -= panel_y

    hoveredPlanet = None  
    max_distance = max((p.distance for p in selectedStar.planets), default=1)  
    start_x = star_x + (selectedStar.starDiameter * 3) + 50
    spacing = (panel_width - start_x - 50) // max(1, len(selectedStar.planets))

    for i, planet in enumerate(selectedStar.planets):
        planet_x = start_x + i * spacing
        planet_y = star_y
        planet_size = max(5, int(round(planet.diameter)))

        planet_rect = pygame.Rect(planet_x - planet_size, planet_y - planet_size, planet_size * 2, planet_size * 2)

        pygame.draw.circle(panel, (0, 255, 0), (planet_x, planet_y), planet_size)

        if hasattr(planet, 'ring') and planet.ring:
            pygame.draw.ellipse(panel, (200, 200, 200), 
                (planet_x - planet_size - 5, planet_y - planet_size // 4, (planet_size + 5) * 2, planet_size // 2), 2)

        moon_x = planet_x
        moon_y = planet_y - planet_size - 10  
        for _ in range(planet.moons):
            pygame.draw.circle(panel, (200, 200, 200), (moon_x, moon_y), 3)
            moon_y -= 10  

        planet_text = font.render(f"P{planet.distance:.1f}", True, (255, 255, 255))
        panel.blit(planet_text, (planet_x - 10, planet_y + planet_size + 5))

        if planet_rect.collidepoint(mouse_x, mouse_y):
            hoveredPlanet = planet  

    # **Planet Details (Bottom Left)**
    if hoveredPlanet:
        details_text = [
            f"Planet Details:",
            f"Distance: {hoveredPlanet.distance:.1f} AU",
            f"Diameter: {hoveredPlanet.diameter:.1f} million km",
            f"Moons: {hoveredPlanet.moons}",
            f"Has Rings: {'Yes' if hasattr(hoveredPlanet, 'ring') and hoveredPlanet.ring else 'No'}"
        ]
        y_offset = panel_height - 100  
        for line in details_text:
            detail_render = font.render(line, True, (255, 255, 255))
            panel.blit(detail_render, (10, y_offset))
            y_offset += 20

    screen.blit(panel, (panel_x, panel_y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
