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
        self.vie = 5
        self.ammo = 2
        self.block = [(22, 14), (23, 14), (22, 15), (23, 15), (25, 14), (24, 14), (25, 15), (24, 15), (1, 0), (22, 16), (22, 17),
 (23, 16), (23, 17),
 (24, 16), (24, 17),
 (25, 16), (25, 17),
 (26, 16), (26, 17),
 (27, 16), (27, 17),
 (28, 16), (28, 17),
 (29, 16), (29, 17),
 (30, 16), (30, 17),
 (31, 16), (31, 17)]

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
        for i in range(self.ammo):
            x = 0+i*12
            y = 0
            pyxel.blt(112-x, y, 0, 0, 200, 16, 16, 5)

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        left_tile = pyxel.tilemap(0).pget(self.x // 8, (new_y + self.size) // 8)
        right_tile = pyxel.tilemap(0).pget((self.x + self.size - 1) // 8, (new_y + self.size) // 8)
        if left_tile == (14, 0) or right_tile == (14, 0):
            new_x = self.x + dx/3
            new_y = self.y + dy/3

        if dx > 0 and not self.check_collision_right(new_x):
            self.x = new_x
        elif dx < 0 and not self.check_collision_left(new_x):
            self.x = new_x

        if dy > 0 and not self.check_collision_below(new_y) and self.y < 116:
            self.y = new_y
        elif dy < 0 and not self.check_collision_above(new_y) and self.y > -2:
            self.y = new_y

    def check_collision_below(self, new_y):
        left_tile = pyxel.tilemap(0).pget(self.x // 8, (new_y + self.size) // 8)
        right_tile = pyxel.tilemap(0).pget((self.x + self.size - 1) // 8, (new_y + self.size) // 8)
        if left_tile in self.block or right_tile in self.block:
            print("oui l'eureka")
            return True
        else:
            return False

    def check_collision_right(self, new_x):
        new_x = new_x - 1
        top_tile = pyxel.tilemap(0).pget((new_x + self.size) // 8, self.y // 8)
        bottom_tile = pyxel.tilemap(0).pget((new_x + self.size) // 8, (self.y + self.size - 1) // 8)
        if top_tile in self.block or bottom_tile in self.block:
            print("oui l'eureka")
            return True
        else:
            return False

    def check_collision_left(self, new_x):
        top_tile = pyxel.tilemap(0).pget((new_x) // 8, self.y // 8)
        bottom_tile = pyxel.tilemap(0).pget((new_x) // 8, (self.y + self.size - 1) // 8)
        if top_tile in self.block or bottom_tile in self.block:
            print("oui l'eureka")
            return True
        else:
            return False

    def check_collision_above(self, new_y):
        left_tile = pyxel.tilemap(0).pget(self.x // 8, new_y // 8)
        right_tile = pyxel.tilemap(0).pget((self.x + self.size - 1) // 8, new_y // 8)
        if left_tile in self.block or right_tile in self.block:
            print("oui l'eureka")
            return True
        else:
            return False


class Ammo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, cam_x, cam_y):
        pyxel.blt(self.x - cam_x, self.y - cam_y, 0, 0, 200, 16, 16, 5)

    def coll_joueur(self, x, y):
        if ((x - self.x)**2 + (y - self.y)**2)**0.5 < 10:
            return True


class Balles:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 0.3

    def update(self):
        self.x += self.speed * self.direction

    def draw(self, cam_x, cam_y):
        pyxel.blt(self.x-cam_x, self.y-cam_y, 0, 64, 56, 16, 16, 5)


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
        self.retour = False
        self.dx = self.dy = random.choice([-1, 1])
        self.zone = False

    def update(self):
        if self.retour:
            dx = self.start_x - self.x
            dy = self.start_y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance < 1:
                self.retour = False
                self.action = False
            else:
                dx /= distance
                dy /= distance
                self.x += dx * self.speed
                self.y += dy * self.speed
                self.direction = 1 if dx > 0 else -1
        elif self.attack:
            dx = player.x - self.x
            dy = player.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > 70:
                self.attack = False
            elif distance < 3:
                player.vie -= 1
                self.retour = True
                self.attack = False
            else:
                dx /= distance
                dy /= distance
                self.x += dx * self.speed * 1.5
                self.y += dy * self.speed * 1.5
                self.direction = 1 if dx > 0 else -1

        else:
            if random.random() < 0.01:
                self.action = True
                angle = random.uniform(0, 2 * math.pi)
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
        if self.zone:
            pyxel.blt(self.x + 4 - cam_x, self.y - 8 - cam_y, 0, 16, 232, 16, 16, 5)
        if self.attack:
            pyxel.blt(self.x + 4 - cam_x, self.y - 8 - cam_y, 0, 32, 232, 16, 16, 5)

    def is_collisions(self, x, y):
        if ((x - self.x-8)**2 + (y - self.y-4)**2)**0.5 < 7:
            return True

    def detect_joueur(self, x, y):
        if not self.retour and ((x - self.x)**2 + (y - self.y)**2)**0.5 < 50:
            self.attack = True
            self.zone = False
            return True

    def detect_joueur_zone(self, x, y):
        if not self.retour and not self.attack and 50 < ((x - self.x)**2 + (y - self.y)**2)**0.5 < 70:
            self.zone = True
        else:
            self.zone = False


class menu:

    def __init__(self):
        self.pause = False
        self.jeu_commence = False

    def update(self):
        if not self.jeu_commence:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.jeu_commence = True
            return

        if pyxel.btnp(pyxel.KEY_P):
            self.pause = not self.pause
        if self.pause:
            return

    #? Main Menu Draw
    def draw(self)-> None:
        pyxel.cls(0)
        if not self.jeu_commence:
            pyxel.text(80, 100, "MP3.2", pyxel.frame_count % 16)
            pyxel.text(60, 130, "Appuyez sur ENTREE pour commencer", 7)
            return

player = Player(10, 55)
Ammos = [Ammo(107, 85), Ammo(287, 40), Ammo(436, 55), Ammo(572, 50), Ammo(808, 24), Ammo(777, 55), Ammo(955, 53), Ammo(1259, 17), Ammo(1359, 58), Ammo(1639, 76)]
spiders = [Spiders(70, 20, 16, 16, 0.8, 15, [0, 16, 32, 48]),
           Spiders(255, 83, 16, 16, 1, 15, [0, 16, 32, 48]),
           Spiders(198, 50, 16, 16, 0.9, 15, [0, 16, 32, 48]),
           Spiders(512, 22, 16, 16, 1.4, 15, [0, 16, 32, 48]),
           Spiders(659, 35, 20, 16, 1.3, 15,  [0, 16, 32, 48]),
           Spiders(745, 75, 16, 16, 1.5, 15, [0, 16, 32, 48]),
           Spiders(923, 21, 16, 16, 1.7, 15, [0, 16, 32, 48]),
           Spiders(1053, 50, 16, 16, 0.8, 15, [0, 16, 32, 48]),
           Spiders(1144, 22, 16, 16, 1.4, 15, [0, 16, 32, 48]),
           Spiders(1498, 27, 16, 16, 1.5, 15, [0, 16, 32, 48]),
           Spiders(1750, 52, 16, 16, 2, 15, [0, 16, 32, 48])]
balles = []

def update():
    global tps
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q):
        player.move(-player.speed, 0)
        player.direction = -1
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
        player.move(player.speed, 0)
        player.direction = 1
    if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z):
        player.move(0, -player.speed)
    if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
        player.move(0, player.speed)
    if pyxel.btn(pyxel.KEY_A):
        print(player.x, player.y)
    if pyxel.btnp(pyxel.KEY_SPACE):
        if player.ammo > 0:
            balles.append(Balles(player.x, player.y, player.direction))
            player.ammo -= 1

    for spider in spiders:
        for balle in balles:
            if spider.is_collisions(balle.x, balle.y):
                spiders.remove(spider)
                balles.remove(balle)
        spider.update()
        for balle in balles:
            balle.update()
            if not 0+player.cam_x< balle.x < 128+player.cam_x:
                balles.remove(balle)
        spider.detect_joueur(player.x, player.y)
        spider.detect_joueur_zone(player.x, player.y)
    for ammo in Ammos:
        if ammo.coll_joueur(player.x, player.y):
            if player.ammo < 5:
                player.ammo += 1
                try:
                    Ammos.remove(ammo)
                except:
                    pass

    update_camera()



def draw():
    pyxel.cls(0)
    cam_x, cam_y = player.cam_x, player.cam_y
    pyxel.bltm(0, 0, 0, cam_x, cam_y, pyxel.width, pyxel.height)
    for spider in spiders:
        spider.draw(cam_x, cam_y)
    for balle in balles:
        balle.draw(cam_x, cam_y)
    player.draw(cam_x, cam_y)
    for i in range(player.vie):
        pyxel.blt(0+i*12, 113, 0, 48, 200, 16, 16, 5)
    for ammo in Ammos:
        ammo.draw(cam_x, cam_y)



def update_camera():
    player.cam_x = max(0, min(player.x - pyxel.width // 4, pyxel.tilemap(0).width * 8 - pyxel.width))



pyxel.run(update, draw)