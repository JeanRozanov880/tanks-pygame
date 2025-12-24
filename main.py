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

    def flip1_blue(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, -90)
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip2_blue(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, 90)
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip3_blue(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, 360)
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip4_blue(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, 180)
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip1_red(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, -90)
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2

    def flip2_red(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, 90)
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2

    def flip3_red(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, 360)
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2

    def flip4_red(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, 180)
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


class Bullet:
    def __init__(self, blue_tank_rect):
        self.bullet_surf = pg.image.load('images/bullet.png').convert_alpha()
        self.bullet_surf = pg.transform.scale(self.bullet_surf,
                                             (self.bullet_surf.get_width() / 8,
                                              self.bullet_surf.get_height() / 8))
        self.bullet_rect = self.bullet_surf.get_rect(center=blue_tank_rect.center)
        self.start_y = blue_tank_rect.centery
        self.flag_active = True

    def is_active(self):
        return self.flag_active

    def fly(self):
        if (self.start_y - self.bullet_rect.y) < 1000:
            self.bullet_rect.y -= speed
        else:
            self.flag_active = False

    def draw(self, screen):
        screen.blit(self.bullet_surf, self.bullet_rect)


pg.init()
screen = pg.display.set_mode((W, H))
pg.display.set_caption("Игра")
clock = pg.time.Clock()
tank = Tank()

bullets = []

flag_play = True
while flag_play:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            flag_play = False
            break
    if not flag_play:
        break

    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        tank.move_1(dx=-1)
        tank.rect_1 = tank.flip2_blue()
    elif keys[pg.K_d]:
        tank.move_1(dx=1)
        tank.rect_1 = tank.flip1_blue()
    elif keys[pg.K_w]:
        tank.move_1(dy=-1)
        tank.rect_1 = tank.flip3_blue()
    elif keys[pg.K_s]:
        tank.move_1(dy=1)
        tank.rect_1 = tank.flip4_blue()
    if keys[pg.K_SPACE]:
        bullets.append(Bullet(tank.rect_1))


    if keys[pg.K_LEFT]:
        tank.move_2(dx=-1)
        tank.rect_2 = tank.flip2_red()
    elif keys[pg.K_RIGHT]:
        tank.move_2(dx=1)
        tank.rect_2 = tank.flip1_red()
    elif keys[pg.K_UP]:
        tank.move_2(dy=-1)
        tank.rect_2 = tank.flip3_red()
    elif keys[pg.K_DOWN]:
        tank.move_2(dy=1)
        tank.rect_2 = tank.flip4_red()

    screen.fill(BG)
    tank.draw(screen)
    for elem in bullets:
        elem.fly()
        elem.draw(screen)

    bullets = [elem for elem in bullets if elem.is_active()]

    pg.display.update()  # обновление экрана, чтобы отобразить новую перерисовку
