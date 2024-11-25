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
        pyxel.rect(self.x, self.y, player.size, player.size, 8)

    def is_collision(self, dx, dy):
        tile_size = 8
        corners = [(0, 0), (self.size - 1, 0), (0, self.size - 1), (self.size - 1, self.size - 1)]
        full_blocks = [(5, 0), (5, 1), (7, 0), (4, 1), (6, 0), (6, 1), (7, 1), (7, 2), (6, 2), (5, 2),
                       (7, 3), (6, 2), (5, 2), (7, 3), (6, 3), (5, 3), (7, 4), (6, 4), (5, 4), (7, 5),
                       (6, 5), (5, 5)]

        for corner in corners:
            tile_x = (dx + corner[0]) // tile_size
            tile_y = (dy + corner[1]) // tile_size

            block_at_position = pyxel.tilemap(0).pget(tile_x, tile_y)

            if block_at_position in full_blocks:
                return True

        return False

player = Player(15, 128)

def update():
    cam_x, cam_y = player.cam_x, player.cam_y
    pyxel.bltm(-cam_x, -cam_y + 1, 0, 0, 0, pyxel.tilemap(0).width * 8, pyxel.tilemap(0).height * 8)
    player.cam_x = max(0, min(player.x - 128 // 2, pyxel.tilemap(0).width * 8 - 128))
    player.cam_y = max(0, min(player.y - 128 // 2, pyxel.tilemap(0).height * 8 - 128))
    if pyxel.btn(pyxel.KEY_LEFT):
        player.move(-player.speed, 0)
    if pyxel.btn(pyxel.KEY_RIGHT):
        player.move(player.speed, 0)
    if pyxel.btn(pyxel.KEY_UP):
        player.move(0, -player.speed)
    if pyxel.btn(pyxel.KEY_DOWN):
        player.move(0, player.speed)
       

def draw():
   pyxel.cls(0)
   player.draw()


pyxel.run(update, draw)