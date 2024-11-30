import random
import math
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
        self.vie = 3
        self.tirs_liste = []
        self.tirs_direction = []

    def draw(self, cam_x, cam_y):
        coeff = pyxel.frame_count // 6 % 6
        coord = (0, 0)
        if 0 <= coeff <= 1:
            coord = (0, 8)
        if 2 <= coeff <= 3:
            coord = (16, 24)
        if 4 <= coeff <= 5:
            coord = (0, 24)
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



class Balles:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y+4
        self.direction = direction
        self.speed = 0.3

    def update(self):
        self.x += self.speed * self.direction

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 32, 8, 8, 8, 5)


class Spiders:
    def __init__(self, x, y, width, height, speed, distance, skin):
        self.x = x
        self.start_x = x
        self.start_y = y
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = 1
        self.distance = distance
        self.skin = skin
        self.action = False
        self.attack = False
        self.retour = False  # Nouvel état pour le retour
        self.dx = self.dy = random.choice([-1, 1])

    def update(self):
        if self.retour:  # Gestion du retour à la position de départ
            dx = self.start_x - self.x
            dy = self.start_y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance < 1:  # Arrêt une fois arrivé à la position de départ
                self.retour = False
                self.action = False
            else:
                dx /= distance
                dy /= distance
                self.x += dx * self.speed
                self.y += dy * self.speed
                self.direction = 1 if dx > 0 else -1

        elif self.attack:  # Comportement d'attaque
            dx = player.x - self.x
            dy = player.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > 70:
                self.attack = False
            elif distance < 3:  # Si collision avec le joueur
                self.retour = True  # Déclenche le retour
                self.attack = False
            else:
                dx /= distance
                dy /= distance
                self.x += dx * self.speed * 1.5
                self.y += dy * self.speed * 1.5
                self.direction = 1 if dx > 0 else -1

        else:  # Mouvement aléatoire
            if random.random() < 0.01:
                self.action = True
                angle = random.uniform(0, 2 * math.pi)  # Angle en radians
                self.dx = math.cos(angle)
                self.dy = math.sin(angle)
            if self.action:
                self.x += self.speed * self.dx
                self.y += self.speed * self.dy
                if ((self.x - self.start_x) ** 2 + (self.y - self.start_y) ** 2) > self.distance ** 2:
                    self.dx *= -1
                    self.dy *= -1
                    self.action = False

    def draw(self, cam_x, cam_y):
        coeff = pyxel.frame_count // 4 % 4
        if coeff == 0:
            pyxel.blt(self.x - cam_x, self.y - cam_y, 0, self.skin[0], 136, self.width * self.direction, self.height, 5)
        if coeff == 1:
            pyxel.blt(self.x - cam_x, self.y - cam_y, 0, self.skin[1], 136, self.width * self.direction, self.height, 5)
        if coeff == 2:
            pyxel.blt(self.x - cam_x, self.y - cam_y, 0, self.skin[2], 136, self.width * self.direction, self.height, 5)
        if coeff == 3:
            pyxel.blt(self.x - cam_x, self.y - cam_y, 0, self.skin[3], 136, self.width * self.direction, self.height, 5)

    def is_collisions(self, x, y):
        if ((x - self.x-player.cam_x)**2 + (y - self.y-player.cam_y)**2)**0.5 < 3:
            self.attack = True
            return True

    def detect_joueur(self, x, y):
        if not self.retour and ((x - self.x)**2 + (y - self.y)**2)**0.5 < 50:
            self.attack = True


player = Player(10, 55)
spiders = [Spiders(70, 20, 16, 16, 0.5, 15, [0, 16, 32, 48]),
           Spiders(255, 83, 16, 16, 1, 15, [0, 16, 32, 48]),
           Spiders(198, 50, 16, 16, 0.2, 15, [0, 16, 32, 48]),
           Spiders(512, 22, 16, 16, 0.4, 15, [0, 16, 32, 48]),
           Spiders(659, 35, 20, 16, 16, 0.5,  [0, 16, 32, 48]),
           Spiders(745, 75, 16, 16, 0.5, 15, [0, 16, 32, 48]),
           Spiders(923, 21, 16, 16, 0.7, 15, [0, 16, 32, 48]),
           Spiders(1053, 50, 16, 16, 0.2, 15, [0, 16, 32, 48]),
           Spiders(1144, 22, 16, 16, 0.4, 15, [0, 16, 32, 48]),
           Spiders(1498, 27, 16, 16, 0.5, 15, [0, 16, 32, 48]),
           Spiders(1750, 52, 16, 16, 0.5, 15, [0, 16, 32, 48])]
balles = []

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
    if pyxel.btn(pyxel.KEY_A):
        print(player.x, player.y)
    if pyxel.btnp(pyxel.KEY_SPACE):
        cam_x, cam_y = player.cam_x, player.cam_y
        balles.append(Balles(player.x-cam_x, player.y-cam_y, player.direction))

    for spider in spiders:
        spider.update()
        if spider.is_collisions(player.x, player.y):
            player.vie -= 1
            spider.retour = True
        for balle in balles:
            balle.update()
            if not 0< balle.x < 128:
                balles.remove(balle)
            if spider.is_collisions(balle.x, balle.y):
                spiders.remove(spider)
                balles.remove(balle)
        spider.detect_joueur(player.x, player.y)

    update_camera()


def draw():
    pyxel.cls(0)
    cam_x, cam_y = player.cam_x, player.cam_y
    pyxel.bltm(0, 0, 0, cam_x, cam_y, pyxel.width, pyxel.height)
    for spider in spiders:
        spider.draw(cam_x, cam_y)
    for balle in balles:
        balle.draw()
    player.draw(cam_x, cam_y)
    pyxel.blt(112, 1, 0, 48, 216, 16, 16, 5)


def update_camera():
    player.cam_x = max(0, min(player.x - pyxel.width // 2, pyxel.tilemap(0).width * 8 - pyxel.width))


pyxel.run(update, draw)