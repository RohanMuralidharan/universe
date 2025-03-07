from lehmer32 import Lehmer

class Planet:
    def __init__(self):
        self.distance = 0.0
        self.diameter = 0.0
        self.foilage = 0.0
        self.minerals = 0.0
        self.water = 0.0
        self.gases = 0.0
        self.temperature = 0.0
        self.life = 0.0
        self.ring = False
        self.population = 0
        self.moons = 0
        self.Moons = []
        self.gravity = 0.0
        self.color = 0xff000000
class starSystem:
    def __init__(self, x, y, z=f"ASTv{15}", generateFullSystem=False):
        self.x = x
        self.y = y
        self.name = z
        self.nlehmer = Lehmer((int(x) & 0xffff) << 16 | (int(y) & 0xffff))
        self.starExists = self.rndInt(0, 20) == 1
        self.temperature = self.rndInt(2000, 50000)
        self.type = "O" if self.temperature > 30000 else "B" if self.temperature > 10000 else "A" if self.temperature > 7500 else "F" if self.temperature > 6000 else "G" if self.temperature > 5000 else "K" if self.temperature > 3500 else "M"

        if(not self.starExists):
            return;
    
        self.starDiameter = self.rndInt(10, 40)
        self.colors = [
            0xffad6242,  # Mars-like (Rusty Red)
            0xffc2b280,  # Earth-like (Sandy Desert)
            0xff8c92ac,  # Mercury-like (Dark Gray)
            0xffddb887,  # Venus-like (Pale Yellowish)
            0xff705b3e,  # Titan-like (Brownish)
            0xff546a76,  # Neptune-like (Muted Cyan)
            0xffe6b800,  # Io-like (Sulfur Yellow)
            0xffc1440e,  # Jupiter-like Bands (Reddish-Orange)
            0xff6a0dad,  # Exotic Purple Planet
            0xff228b22,  # Verdant Green (Alien Forest)
        ]
        self.starColor = self.colors[self.rndInt(0, len(self.colors) - 1)]

        if(not generateFullSystem):
            return
        
        self.distanceFromStar = self.rndInt(60, 200)
        self.nPlanets = self.rndInt(0, 9)
        self.planets = []
        
        for i in range(self.nPlanets):
            p = Planet()
            p.distance = self.distanceFromStar + i * self.rndDouble(10, 30)
            p.diameter = max(2, min(self.rndDouble(2, 22), 22))  # Keep within expected range

            p.foilage = self.rndDouble(0, 1)
            p.minerals = self.rndDouble(0, 1)
            p.water = self.rndDouble(0, 1)
            p.gases = self.rndDouble(0, 1)
            p.temperature = self.rndDouble(-100, 100)
            p.life = self.rndDouble(0, 1)
            p.ring = self.rndInt(0, 20) > 18
            p.population = self.rndInt(0, 1000000000)
            p.gravity = self.rndDouble(0, 20)
            p.moons = max(self.rndInt(-5, 7), 0)

            for i in range(p.moons):
                p.Moons.append(self.rndDouble(1, 5))
            dSum = 1.0 / (p.foilage + p.minerals + p.water + p.gases)
            p.foilage *= dSum
            p.minerals *= dSum
            p.water *= dSum
            p.gases *= dSum
            self.planets.append(p)

    def rndInt(self, min, max):
        return self.nlehmer.Lehmer() % (max - min + 1) + min
    
    def rndDouble(self, min, max):
        return (self.nlehmer.Lehmer() % 0xffffffff) / 0xffffffff * (max - min) + min


