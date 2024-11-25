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
            
    def draw(self, cam_x, cam_y):
        #pyxel.rect(self.x, self.y, player.size, player.size, 8)
        coeff = pyxel.frame_count // 4 % 4
        if coeff == 0:
            coord = (0, 8)
        if coeff == 1:
            coord = (16, 8)
        if coeff == 2:
            coord = (0, 24)
        if coeff == 3:
            coord = (16, 24)
        pyxel.blt(self.x - cam_x, self.y - cam_y + 1, 0, coord[0], coord[1], 16, 16, 5)

    def is_collision(self, dx, dy):
        tile_size = 16 
        corners = [(0, 0), (self.size - 1, 0), (0, self.size - 1), (self.size - 1, self.size - 1)]
        full_blocks = [(1, 0), (24, 15), (22, 14), (22, 16), (24, 16), (28, 16), (240, 128)]  # Tuiles solides
        
        for corner in corners:
            tile_x = (self.x + dx + corner[0]) // tile_size 
            tile_y = (self.y + dy + corner[1]) // tile_size  
            
            block_at_position = pyxel.tilemap(0).pget(tile_x, tile_y)
            print(block_at_position)
            # Vérifier si la tuile à la position calculée est un full block (solide)
            if block_at_position in full_blocks:
                return True  # Collision détectée

        return False  # Aucune collision

class Spider:
    def init(x, y)
        self.x = x
        self.y = y
        self.cam_x = 0
        self.cam_y = 0
        self.speed = 2
        self.size = 8
        self.direction = 1
        
    def draw(self, cam_x, cam_y):
        coeff = pyxel.frame_count // 4 % 4
        if coeff == 0:
            coord = (0, 8)
        if coeff == 1:
            coord = (16, 8)
        if coeff == 2:
            coord = (0, 24)
        if coeff == 3:
            coord = (16, 24)
        pyxel.blt(self.x - cam_x, self.y - cam_y + 1, 0, coord[0], coord[1], 16, 16, 5)

    def move(self, dx, dy):
         if not self.is_collision(self.x + dx, self.y + dy):
            if dx < 0:
               self.direction = -1
            elif dx > 0:
               self.direction = 1
            self.x += dx
            self.y += dy

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
   cam_x, cam_y = player.cam_x, player.cam_y
   pyxel.bltm(-cam_x, -cam_y + 1, 0, 0, 0, pyxel.tilemap(0).width * 8, pyxel.tilemap(0).height * 8)
   player.draw(cam_x, cam_y)

pyxel.run(update, draw)
