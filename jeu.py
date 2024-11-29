import pyxel

pyxel.init(128, 128, title="Projet 3.2")
pyxel.fullscreen(False)
pyxel.load("data.pyxres")


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cam_x = 0
        self.cam_y = 0
        self.speed = 1
        self.size = 16
        self.direction = 1
        self.tirs_liste = []
        self.tirs_direction = 1
        self.bonus_liste = []

    def draw(self, cam_x, cam_y):
        coeff = pyxel.frame_count // 4 % 4
        coord = (0, 0)
        if coeff == 0:
            coord = (0, 8)
        if coeff == 1:
            coord = (16, 8)
        if coeff == 2:
            coord = (0, 24)
        if coeff == 3:
            coord = (16, 24)
        pyxel.blt(self.x - cam_x, self.y - cam_y + 1, 0, coord[0], coord[1], 16*self.direction, 16, 5)

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if dx > 0 and not self.check_collision_right(new_x):
            self.x = new_x
        elif dx < 0 and not self.check_collision_left(new_x):
            self.x = new_x

        if dy > 0 and not self.check_collision_below(new_y):
            self.y = new_y
        elif dy < 0 and not self.check_collision_above(new_y):
            self.y = new_y

    def check_collision_below(self, new_y):
        left_tile = pyxel.tilemap(0).pget(self.x // 8, (new_y + self.size) // 8)
        right_tile = pyxel.tilemap(0).pget((self.x + self.size - 1) // 8, (new_y + self.size) // 8)
        print(left_tile, right_tile)
        return left_tile[0] == 1 or right_tile[0] == 1

    def check_collision_right(self, new_x):
        new_x = new_x - 1
        top_tile = pyxel.tilemap(0).pget((new_x + self.size) // 8, self.y // 8)
        bottom_tile = pyxel.tilemap(0).pget((new_x + self.size) // 8, (self.y + self.size - 1) // 8)
        return top_tile[0] == 1 or bottom_tile[0] == 1

    def check_collision_left(self, new_x):
        top_tile = pyxel.tilemap(0).pget((new_x) // 8, self.y // 8)
        bottom_tile = pyxel.tilemap(0).pget((new_x) // 8, (self.y + self.size - 1) // 8)
        return top_tile[0] == 1 or bottom_tile[0] == 1

    def check_collision_above(self, new_y):
        left_tile = pyxel.tilemap(0).pget(self.x // 8, new_y // 8)
        right_tile = pyxel.tilemap(0).pget((self.x + self.size - 1) // 8, new_y // 8)
        return left_tile[0] == 1 or right_tile[0] == 1

    def tirs(self):
        if pyxel.btnr(pyxel.KEY_SPACE):
            if self.tirs_direction == 1:
                self.tirs_liste.append([self.x + 8, self.y + 4])
            elif self.tirs_direction == -1:
                self.tirs_liste.append([self.x -8, self.y + 4])

    def tirs_droit(self):
        for tir in self.tirs_liste: # si le joueur regarde vers la droite
                tir[0] += 4
                if tir[0] < -128 or tir[0] > 128:
                    self.tirs_liste.remove(tir)

    def tirs_gauche(self):
        for tir in self.tirs_liste: # si le joueur regarde vers la gauche
                tir[0] -= 4
                if tir[0] < -120 or tir[0] > 120:
                    self.tirs_liste.remove(tir)

    def bonus_creation(self):
        if pyxel.frame_count % 200 == 0:
            bonus_type = random.choice(["vie", "tir", "grenade"])
            x_position = # a voir
            y_position = # a voir
            self.bonus_liste.append({"type": bonus_type, "x": x_position, "y": y_position})


player = Player(10, 55)

def update():
    if pyxel.btn(pyxel.KEY_LEFT):
        player.move(-player.speed, 0)
        player.direction = -1
    if pyxel.btn(pyxel.KEY_RIGHT):
        player.move(player.speed, 0)
        player.direction = 1
    if pyxel.btn(pyxel.KEY_UP):
        player.move(0, -player.speed)
    if pyxel.btn(pyxel.KEY_DOWN):
        player.move(0, player.speed)
    update_camera()
    
    if pyxel.btn(pyxel.KEY_LEFT):
        player.tirs_direction = -1
    if pyxel.btn(pyxel.KEY_RIGHT):
        player.tirs_direction = 1

    player.tirs()
    if player.tirs_direction == 1:
        player.tirs_droit()
    if player.tirs_direction == -1:
        player.tirs_gauche()


def draw():
    pyxel.cls(0)
    cam_x, cam_y = player.cam_x, player.cam_y
    pyxel.bltm(0, 0, 0, cam_x, cam_y, pyxel.width, pyxel.height)
    player.draw(cam_x, cam_y)

    for tir in player.tirs_liste:
         pyxel.blt(tir[0], tir[1], 0, 32, 8, 8, 8)


def update_camera():
    player.cam_x = max(0, min(player.x - pyxel.width // 2, pyxel.tilemap(0).width * 8 - pyxel.width))


pyxel.run(update, draw)
