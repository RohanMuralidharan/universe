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
class starSystem:
    def __init__(self, x, y, z=0, generateFullSystem=False):
        self.x = x
        self.y = y
        self.z = z
        self.nlehmer = Lehmer((int(x) & 0xffff) << 16 | (int(y) & 0xffff))
        self.starExists = self.rndInt(0, 20) > 18

        if(not self.starExists):
            return;
    
        self.starDiameter = self.rndInt(10, 40)
        self.colors = [0xffffffff, 0xffd9ffff, 0xffa3ffff, 0xffffc8c8, 0xffffcb9d, 0xff415eff, 0xff28199d]
        self.starColor = self.colors[self.rndInt(0, len(self.colors) - 1)]

        if(not generateFullSystem):
            return
        
        self.distanceFromStar = self.rndInt(60, 200)
        self.nPlanets = self.rndInt(0, 12)
        self.planets = []
        
        for i in range(self.nPlanets):
            p = Planet()
            p.distance = self.distanceFromStar + i * self.rndDouble(10, 30)
            p.diameter = self.rndDouble(2, 22)
            p.foilage = self.rndDouble(0, 1)
            p.minerals = self.rndDouble(0, 1)
            p.water = self.rndDouble(0, 1)
            p.gases = self.rndDouble(0, 1)
            p.temperature = self.rndDouble(-100, 100)
            p.life = self.rndDouble(0, 1)
            p.ring = self.rndInt(0, 20) > 18
            p.population = self.rndInt(0, 1000000000)
            p.gravity = self.rndDouble(0, 20)
            p.moons = max(self.rndInt(-5, 10), 0)

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
        return self.nlehmer.Lehmer() / 0xffffffff * (max - min) + min

