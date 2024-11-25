import pyxel

pyxel.init(256, 256, title="Projet 3.2")
pyxel.fullscreen(False)
pyxel.load("data.pyxres")


def draw():
   pyxel.cls(0)

def update():
   pass

pyxel.run(update, draw)