import pygame as pg

FPS = 60
W, H = 1000, 1000
BG = (100, 170, 220)
speed = 3
bullet_speed = 6


class Tank:
    def __init__(self):
        # Загрузка и масштабирование синего танка
        self.surf_1 = pg.image.load('images/blue_tank.png').convert_alpha()
        self.new_surf_1 = pg.transform.scale(self.surf_1,
                                             (self.surf_1.get_width() / 8,
                                              self.surf_1.get_height() / 8))
        self.surf_1 = self.new_surf_1
        self.rect_1 = self.new_surf_1.get_rect(center=(W / 6, H / 4))
        self.direction_1 = 0

        # Загрузка и масштабирование красного танка
        self.surf_2 = pg.image.load('images/red_tank.png').convert_alpha()
        self.new_surf_2 = pg.transform.scale(self.surf_2,
                                             (self.surf_2.get_width() / 8,
                                              self.surf_2.get_height() / 8))
        self.surf_2 = self.new_surf_2
        self.rect_2 = self.new_surf_2.get_rect(center=(W / 1.5, H / 1.5))
        self.direction_2 = 0
        self.cnt_iters = 0

    def flip1_blue(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, -90)  # вправо
        self.direction_1 = 90
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip2_blue(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, 90)  # влево
        self.direction_1 = 270
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip3_blue(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, 360)  # вверх
        self.direction_1 = 0
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip4_blue(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, 180)  # вниз
        self.direction_1 = 180
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip1_red(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, -90)  # вправо
        self.direction_2 = 90
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2

    def flip2_red(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, 90)  # влево
        self.direction_2 = 270
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2

    def flip3_red(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, 360)  # вверх
        self.direction_2 = 0
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2

    def flip4_red(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, 180)  # вниз
        self.direction_2 = 180
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
        self.cnt_iters += 1
        screen.blit(self.new_surf_1, self.rect_1)
        screen.blit(self.new_surf_2, self.rect_2)

    def can_shoot(self):
        return self.cnt_iters >= 40

    def shoot(self):
        self.cnt_iters = 0


class Bullet:
    def __init__(self, tank_rect, direction, tank_type=1):
        self.bullet_surf = pg.image.load('images/bullet.png').convert_alpha()
        self.bullet_surf = pg.transform.scale(self.bullet_surf,
                                              (self.bullet_surf.get_width() / 16,
                                               self.bullet_surf.get_height() / 16))

        #  поворачиваем пулю в зависимости от направления
        if direction == 90:  # вправо
            self.bullet_surf = pg.transform.rotate(self.bullet_surf, -90)
        elif direction == 270:  # влево
            self.bullet_surf = pg.transform.rotate(self.bullet_surf, 90)
        elif direction == 180:  # вниз
            self.bullet_surf = pg.transform.rotate(self.bullet_surf, 180)
        # для направления 0 (вверх) не поворачиваем

        #  позиционируем пулю в зависимости от направления и типа танка
        if tank_type == 1:  # синий танк
            if direction == 0:  # вверх
                self.bullet_rect = self.bullet_surf.get_rect(
                    center=(tank_rect.centerx, tank_rect.top)
                )
            elif direction == 90:  # вправо
                self.bullet_rect = self.bullet_surf.get_rect(
                    center=(tank_rect.right, tank_rect.centery)
                )
            elif direction == 180:  # вниз
                self.bullet_rect = self.bullet_surf.get_rect(
                    center=(tank_rect.centerx, tank_rect.bottom)
                )
            elif direction == 270:  # влево
                self.bullet_rect = self.bullet_surf.get_rect(
                    center=(tank_rect.left, tank_rect.centery)
                )
        else:  # красный танк
            if direction == 0:  # вверх
                self.bullet_rect = self.bullet_surf.get_rect(
                    center=(tank_rect.centerx, tank_rect.top)
                )
            elif direction == 90:  # вправо
                self.bullet_rect = self.bullet_surf.get_rect(
                    center=(tank_rect.right, tank_rect.centery)
                )
            elif direction == 180:  # вниз
                self.bullet_rect = self.bullet_surf.get_rect(
                    center=(tank_rect.centerx, tank_rect.bottom)
                )
            elif direction == 270:  # влево
                self.bullet_rect = self.bullet_surf.get_rect(
                    center=(tank_rect.left, tank_rect.centery)
                )

        self.direction = direction
        self.flag_active = True
        self.travel_distance = 0
        self.max_distance = 950  # максимальная дистанция полета пули

    def is_active(self):
        return self.flag_active

    def fly(self):
        # Двигаем пулю в зависимости от направления
        if self.direction == 0:  # вверх
            self.bullet_rect.y -= bullet_speed
        elif self.direction == 90:  # вправо
            self.bullet_rect.x += bullet_speed
        elif self.direction == 180:  # вниз
            self.bullet_rect.y += bullet_speed
        elif self.direction == 270:  # влево
            self.bullet_rect.x -= bullet_speed

        # Проверяем границы экрана
        if (self.bullet_rect.right < 0 or self.bullet_rect.left > W or
                self.bullet_rect.bottom < 0 or self.bullet_rect.top > H):
            self.flag_active = False

        # Проверяем максимальную дистанцию
        self.travel_distance += bullet_speed
        if self.travel_distance >= self.max_distance:
            self.flag_active = False

    def draw(self, screen):
        screen.blit(self.bullet_surf, self.bullet_rect)


class Heart:
    def __init__(self):
        self.heart_surf = pg.image.load('images/heart.png').convert_alpha()
        self.new_heart_surf = pg.transform.scale(self.heart_surf,
                                             (self.heart_surf.get_width() / 8,
                                              self.heart_surf.get_height() / 8))
        self.heart_surf = self.new_heart_surf
        self.heart_rect = self.new_heart_surf.get_rect(center=(W / 6, H / 4))

    def draw(self, screen):
        screen.blit(self.heart_surf, self.heart_rect)



pg.init()
screen = pg.display.set_mode((W, H))
pg.display.set_caption("Игра")
clock = pg.time.Clock()
tank = Tank()

bullets_blue = []  # пули синего танка
bullets_red = []  # пули красного танка

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

    #  управление синим танком
    if keys[pg.K_a]:
        tank.move_1(dx=-1)
        tank.rect_1 = tank.flip2_blue()
    if keys[pg.K_d]:
        tank.move_1(dx=1)
        tank.rect_1 = tank.flip1_blue()
    if keys[pg.K_w]:
        tank.move_1(dy=-1)
        tank.rect_1 = tank.flip3_blue()
    if keys[pg.K_s]:
        tank.move_1(dy=1)
        tank.rect_1 = tank.flip4_blue()

    #  стрельба синего танка
    if keys[pg.K_SPACE] and tank.can_shoot():
        tank.shoot()
        bullets_blue.append(Bullet(tank.rect_1, tank.direction_1, 1))

    #  управление красным танком
    if keys[pg.K_LEFT]:
        tank.move_2(dx=-1)
        tank.rect_2 = tank.flip2_red()
    if keys[pg.K_RIGHT]:
        tank.move_2(dx=1)
        tank.rect_2 = tank.flip1_red()
    if keys[pg.K_UP]:
        tank.move_2(dy=-1)
        tank.rect_2 = tank.flip3_red()
    if keys[pg.K_DOWN]:
        tank.move_2(dy=1)
        tank.rect_2 = tank.flip4_red()

    if keys[pg.K_KP_ENTER] and tank.can_shoot():
        tank.shoot()
        bullets_red.append(Bullet(tank.rect_2, tank.direction_2, 2))

    screen.fill(BG)
    tank.draw(screen)

    for bullet in bullets_blue:
        bullet.fly()
        bullet.draw(screen)

    for bullet in bullets_red:
        bullet.fly()
        bullet.draw(screen)

    #  удаление неактивных пуль
    bullets_blue = [bullet for bullet in bullets_blue if bullet.is_active()]
    bullets_red = [bullet for bullet in bullets_red if bullet.is_active()]

    pg.display.update()
