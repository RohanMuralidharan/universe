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
    selected_planet = None
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
        # Define realistic planet colors
        planet_colors = [
            (139, 69, 19),   # Brown
            (160, 82, 45),   # Sienna
            (205, 133, 63),  # Peru
            (210, 180, 140), # Tan
            (244, 164, 96),  # Sandy Brown
            (222, 184, 135), # Burly Wood
            (255, 228, 181), # Moccasin
            (255, 222, 173), # Navajo White
            (255, 218, 185), # Peach Puff
            (255, 228, 196), # Bisque
            (255, 235, 205), # Blanched Almond
            (255, 239, 213), # Papaya Whip
            (255, 245, 238), # Seashell
            (255, 250, 240), # Floral White
            (255, 255, 240), # Ivory
            (240, 255, 255), # Azure
            (240, 248, 255), # Alice Blue
            (230, 230, 250), # Lavender
            (255, 240, 245), # Lavender Blush
            (255, 228, 225), # Misty Rose
            (128, 0, 128),   # Purple
            (0, 128, 0),     # Green
            (0, 255, 255),   # Cyan
            (255, 0, 255),   # Magenta
            (255, 165, 0),   # Orange
            (255, 20, 147),  # Deep Pink
            (75, 0, 130),    # Indigo
            (0, 255, 0),     # Lime
            (255, 255, 0)    # Yellow
        ]

        lehmer = Lehmer(int(planet.diameter))
        planet.color = planet_colors[lehmer.randInt(0, len(planet_colors) - 1)]

        planet_x = start_x + i * spacing
        planet_y = star_y
        planet_size = max(5, int(round(planet.diameter)))

        planet_rect = pygame.Rect(planet_x - planet_size, planet_y - planet_size, planet_size * 2, planet_size * 2)

        pygame.draw.circle(panel, planet.color , (planet_x, planet_y), planet_size)

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
            hoveredPlanet_x = planet_x
            hoveredPlanet_y = planet_y  
            hoveredPlanet = planet

    if hoveredPlanet:
        details_text = [
            f"Planet Details:",
            f"Distance: {hoveredPlanet.distance:.1f} AU",
            f"Diameter: {hoveredPlanet.diameter:.1f} million km",
            f"Moons: {hoveredPlanet.moons}",
            f"Has Rings: {'Yes' if hasattr(hoveredPlanet, 'ring') and hoveredPlanet.ring else 'No'}"
        ]
        pygame.draw.circle(panel, (255, 255, 255), (hoveredPlanet_x, hoveredPlanet_y), hoveredPlanet.diameter + 3, 2)
        y_offset = panel_height - 100  
        for line in details_text:
            detail_render = font.render(line, True, (255, 255, 255))
            panel.blit(detail_render, (10, y_offset))
            y_offset += 20

            if pygame.mouse.get_pressed()[0] and hoveredPlanet:
                selected_planet = hoveredPlanet
                
    if selected_planet:
        stay = True
        while stay:
            stay = draw_planet_info(selected_planet)

    screen.blit(panel, (panel_x, panel_y))

planetOffset = [0, 0]

def draw_planet_info(planet):
    global planetOffset

    panel_width, panel_height = 1000, 1000
    panel_x, panel_y = 0, 0

    panel = pygame.Surface((panel_width, panel_height))
    panel.fill((0, 0, 0))

    font = pygame.font.Font(None, 24)

    keys = pygame.key.get_pressed()
    speed = 100  
    elapsedTime = clock.get_time() / 24  

    if keys[pygame.K_LEFT]:
        planetOffset[0] += speed * elapsedTime
    if keys[pygame.K_RIGHT]:
        planetOffset[0] -= speed * elapsedTime
    if keys[pygame.K_UP]:
        planetOffset[1] += speed * elapsedTime
    if keys[pygame.K_DOWN]:
        planetOffset[1] -= speed * elapsedTime

    planet_x = panel_width // 2 + planetOffset[0]
    planet_y = panel_height // 2 + planetOffset[1]

    planet_size = max(400, int(round(planet.diameter)) * 4)


    if hasattr(planet, 'ring') and planet.ring:

        ring_colors = [
            (169, 169, 169),  # Dark Gray
            (211, 211, 211),  # Light Gray
            (192, 192, 192),  # Silver
            (255, 215, 0),    # Gold
            (205, 133, 63),   # Peru
            (255, 165, 0),    # Orange
            (255, 69, 0),     # Red-Orange
            (255, 255, 255)   # White
        ]

        lhmr = Lehmer(int(planet.diameter))
        ring_color = ring_colors[lhmr.randInt(0, len(ring_colors) - 1)]
        ring_thickness = lhmr.randInt(15, 50)

        # Draw the back part of the ring (hidden behind the planet)
        pygame.draw.arc(panel, ring_color, 
            (planet_x - planet_size - 40, planet_y - planet_size // 4, (planet_size + 40) * 2, planet_size // 2), 
            math.pi, 2 * math.pi, ring_thickness)
        # Draw the planet on top to hide the back part of the ring
        pygame.draw.circle(panel, planet.color, (planet_x, planet_y), planet_size)
        # Draw the front part of the ring
        pygame.draw.arc(panel, ring_color, 
            (planet_x - planet_size - 40, planet_y - planet_size // 4, (planet_size + 40) * 2, planet_size // 2), 
            0, math.pi, 15)
    else:
        pygame.draw.circle(panel, planet.color, (planet_x, planet_y), planet_size)

    lehmer = Lehmer(int(planet.diameter))
    for _ in range(planet.moons):
        moon_distance = lehmer.randInt(planet_size + 150, planet_size + 300)
        moon_angle = lehmer.uniform(0, 2 * math.pi)
        moon_size = lehmer.randInt(15, 30)

        moon_x = planet_x + int(moon_distance * math.cos(moon_angle))
        moon_y = planet_y + int(moon_distance * math.sin(moon_angle))

        pygame.draw.circle(panel, (200, 200, 200), (moon_x, moon_y), moon_size)

    title_text = font.render("Planet Details", True, (255, 255, 255))
    panel.blit(title_text, (10, 10))

    planet_details = [
        f"Distance: {planet.distance:.1f} AU",
        f"Diameter: {planet.diameter:.1f} million km",
        f"Moons: {planet.moons}",
        f"Has Rings: {'Yes' if hasattr(planet, 'ring') and planet.ring else 'No'}"
    ]

    y_offset = 40
    for line in planet_details:
        detail_render = font.render(line, True, (255, 255, 255))
        panel.blit(detail_render, (10, y_offset))
        y_offset += 20

    screen.blit(panel, (panel_x, panel_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return False

    pygame.display.flip()
    clock.tick(FPS)
    return True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
