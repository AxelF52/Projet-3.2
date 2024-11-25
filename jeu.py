import pyxel

pyxel.init(256, 256, title="Projet 3.2")
pyxel.fullscreen(False)
pyxel.load("data.pyxres")


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
            
    def draw(self):
        pyxel.draw

player = Player(0, 0)

def update():
    cam_x, cam_y = player.cam_x, player.cam_y
    pyxel.bltm(-cam_x, -cam_y + 1, 0, 0, 0, pyxel.tilemap(0).width * 8, pyxel.tilemap(0).height * 8)
    player.cam_x = max(0, min(player.x - 128 // 2, pyxel.tilemap(0).width * 8 - 128))
    player.cam_y = max(0, min(player.y - 128 // 2, pyxel.tilemap(0).height * 8 - 128))
    if pyxel.btnp(pyxel.KEY_LEFT):
        player.move(-player.speed, 0)
    if pyxel.btnp(pyxel.KEY_RIGHT):
        player.move(player.speed, 0)
    if pyxel.btnp(pyxel.KEY_UP):
        player.move(0, 15)
    if not player.y < 1:
        player.y -= 1
       

def draw():
   pyxel.cls(0)
   player.drawn()


pyxel.run(update, draw)