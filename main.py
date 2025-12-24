import pygame as pg

FPS = 60
W, H = 1000, 1000
BG = (100, 170, 220)
speed = 3


class Tank:
    def __init__(self):
        self.surf_1 = pg.image.load('images/blue_tank.png').convert_alpha()
        self.new_surf_1 = pg.transform.scale(self.surf_1,
                                  (self.surf_1.get_width() / 8,
                                   self.surf_1.get_height() / 8))
        self.surf_1 = self.new_surf_1
        self.rect_1 = self.new_surf_1.get_rect(center=(W / 6, H / 4))

        self.surf_2 = pg.image.load('images/red_tank.png').convert_alpha()
        self.new_surf_2 = pg.transform.scale(self.surf_2,
                                  (self.surf_2.get_width() / 8,
                                   self.surf_2.get_height() / 8))
        self.surf_2 = self.new_surf_2
        self.rect_2 = self.new_surf_2.get_rect(center=(W / 1.5, H / 1.5))

    def rotate_tank_1(self, angle):
        rotated = pg.transform.rotate(self.new_surf_1, angle)
        self.new_surf_1 = rotated
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def rotate_tank_2(self, angle):
        rotated = pg.transform.rotate(self.new_surf_2, angle)
        self.new_surf_2 = rotated
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2


    def move_1(self, dx=0, dy=0):
        if (self.rect_1.left + dx * speed) > 0 and (self.rect_1.right + dx * speed) < W:
            self.rect_1.x += dx * speed
        if (self.rect_1.top + dy * speed) > 0 and (self.rect_1.bottom + dy * speed) < H:
            self.rect_1.y += dy * speed

    def move_2(self, dx=0, dy=0):
        if (self.rect_2.left + dx * speed) > 0 and (self.rect_2.right + dx * speed) < W:
            self.rect_2.x += dx * speed
        if (self.rect_2.top + dy * speed) > 0 and (self.rect_2.bottom + dy * speed) < H:
            self.rect_2.y += dy * speed

    def draw(self, screen):
        screen.blit(self.new_surf_1, self.rect_1)
        screen.blit(self.new_surf_2, self.rect_2)

pg.init()
screen = pg.display.set_mode((W, H))
pg.display.set_caption("Игра")
clock = pg.time.Clock()
tank = Tank()

flag_play = True
while flag_play:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            flag_play = False

    keys = pg.key.get_pressed()
    #  управление первым (синим) танком
    if keys[pg.K_LEFT]:
        tank.move_1(dx=-1)
        tank.rotate_tank_1(90)  # Влево
    elif keys[pg.K_RIGHT]:
        tank.move_1(dx=1)
        tank.rotate_tank_1(-90)  # Вправо
    elif keys[pg.K_UP]:
        tank.move_1(dy=-1)
        tank.rotate_tank_1(360)  # Вверх
    elif keys[pg.K_DOWN]:
        tank.move_1(dy=1)
        tank.rotate_tank_1(180)  # Вниз

    #  управление вторым (красным) танком
    if keys[pg.K_a]:
        tank.move_2(dx=-1)
        tank.rotate_tank_2(90)  # Влево
    elif keys[pg.K_d]:
        tank.move_2(dx=1)
        tank.rotate_tank_2(-90)  # Вправо
    elif keys[pg.K_w]:
        tank.move_2(dy=-1)
        tank.rotate_tank_2(360)  # Вверх
    elif keys[pg.K_s]:
        tank.move_2(dy=1)
        tank.rotate_tank_2(180)  # Вниз


    screen.fill(BG)
    tank.draw(screen)
    pg.display.update()

pg.quit()
