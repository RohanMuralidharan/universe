class Lehmer:
    def __init__(self, num=0):
        self.nLehmer = num

    def seed(self, num):
        self.nLehmer = num

    def Lehmer(self):
        self.nLehmer += 0xe120fc15
        tmp =  self.nLehmer * 0x4a39b70d
        m1 = tmp >> 32 ^ tmp
        tmp =  m1 * 0x1fad5c9
        m2 = tmp >> 32 ^ tmp
        return m2