import pyxel

pyxel.init(256, 256, title="Projet 3.2")
pyxel.fullscreen(False)
pyxel.load("data.pyxres")


def draw():
   pyxel.cls(0)

def update():
   pass

class Player:
    """
    Joueur : collisions et mouvements
    """
    def __init__(self, x, y):
        global tps
        self.x = x
        self.y = y
        self.cam_x = 0
        self.cam_y = 0
        self.speed = 2
        self.size = 8
        self.direction = 1

    def move(self, dx, dy):
         if not self.is_collision(self.x + dx, self.y + dy):
            if dx < 0:
               self.direction = -1
            elif dx > 0:
               self.direction = 1
            self.x += dx
            self.y += dy


pyxel.run(update, draw)