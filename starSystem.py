from lehmer32 import Lehmer

class starSystem:

    

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.nlehmer = Lehmer((int(x) & 0xffff) << 16 | (int(y) & 0xffff))
        self.starExists = self.rndInt(0, 20) > 18
        if(not self.starExists):
            return;
        self.starDiameter = self.rndInt(8, 30)
        self.colors = [0xffffffff, 0xffd9ffff, 0xffa3ffff, 0xffffc8c8, 0xffffcb9d, 0xff415eff, 0xff28199d]
        self.starColor = self.colors[self.rndInt(0, len(self.colors) - 1)]

    def rndInt(self, min, max):
        return self.nlehmer.Lehmer() % (max - min + 1) + min
    