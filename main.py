import pygame as pg


FPS = 60
W, H = 1000, 1000
BG = (100, 170, 220)
speed = 3
bullet_speed = 6
HEART_SIZE = 40
MAX_LIVES = 3
HEART_SPACING = 10
waiting_for_choose = True


class Tank:
    def __init__(self, player1, player2):
        if player1 is None:
            player1 = 'images/blue_tank.png'  # скин по умолчанию для 1-го игрока
        if player2 is None:
            player2 = 'images/red_tank.png'  # скин по умолчанию для 2-го игрока

        # загрузка и масштабирование танка 1-го игрока
        self.surf_1 = pg.image.load(player1).convert_alpha()
        self.new_surf_1 = pg.transform.scale(self.surf_1,
                                             (self.surf_1.get_width() / 8,
                                              self.surf_1.get_height() / 8))
        self.surf_1 = self.new_surf_1
        self.rect_1 = self.new_surf_1.get_rect(center=(W / 12, H / 7))
        self.mask_1 = pg.mask.from_surface(self.surf_1)
        self.direction_1 = 0

        # загрузка и масштабирование танка 2-го игрока
        self.surf_2 = pg.image.load(player2).convert_alpha()
        self.new_surf_2 = pg.transform.scale(self.surf_2,
                                             (self.surf_2.get_width() / 8,
                                              self.surf_2.get_height() / 8))
        self.surf_2 = self.new_surf_2
        self.rect_2 = self.new_surf_2.get_rect(center=(W / 1.1, H / 1.1))
        self.mask_2 = pg.mask.from_surface(self.surf_2)
        self.direction_2 = 0
        self.cnt_iters = 0

    def flip1_player1(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, -90)  # вправо
        self.mask_1 = pg.mask.from_surface(self.new_surf_1)
        self.direction_1 = 90
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip2_player1(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, 90)  # влево
        self.mask_1 = pg.mask.from_surface(self.new_surf_1)
        self.direction_1 = 270
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip3_player1(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, 0)  # вверх
        self.mask_1 = pg.mask.from_surface(self.new_surf_1)
        self.direction_1 = 0
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip4_player1(self):
        self.new_surf_1 = pg.transform.rotate(self.surf_1, 180)  # вниз
        self.mask_1 = pg.mask.from_surface(self.new_surf_1)
        self.direction_1 = 180
        current_rect_1 = self.new_surf_1.get_rect(center=self.rect_1.center)
        return current_rect_1

    def flip1_player2(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, -90)  # вправо
        self.mask_2 = pg.mask.from_surface(self.new_surf_2)
        self.direction_2 = 90
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2

    def flip2_player2(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, 90)  # влево
        self.mask_2 = pg.mask.from_surface(self.new_surf_2)
        self.direction_2 = 270
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2

    def flip3_player2(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, 0)  # вверх
        self.mask_2 = pg.mask.from_surface(self.new_surf_2)
        self.direction_2 = 0
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2

    def flip4_player2(self):
        self.new_surf_2 = pg.transform.rotate(self.surf_2, 180)  # вниз
        self.mask_2 = pg.mask.from_surface(self.new_surf_2)
        self.direction_2 = 180
        current_rect_2 = self.new_surf_2.get_rect(center=self.rect_2.center)
        return current_rect_2

    def move_1(self, dx=0, dy=0, wood_boxes=None, metal_boxes=None):
        if wood_boxes is None or metal_boxes is None:
            return

        old_rect = self.rect_1.copy()

        # попытка движения
        if (self.rect_1.left + dx * speed) > 0 and (self.rect_1.right + dx * speed) < W:
            self.rect_1.x += dx * speed
        if (self.rect_1.top + dy * speed) > 0 and (self.rect_1.bottom + dy * speed) < H:
            self.rect_1.y += dy * speed

        collided = False

        # используем первый элемент списков wood_boxes и metal_boxes
        wood_box = wood_boxes[0]
        metal_box = metal_boxes[0]

        # проверяем столкновения с деревянными коробками
        for obs_rect in wood_box.get_all_obstacle_rects():
            if self.rect_1.colliderect(obs_rect):
                offset = (obs_rect.left - self.rect_1.left, obs_rect.top - self.rect_1.top)
                if self.mask_1.overlap_area(wood_box.get_obstacle_mask(obs_rect), offset) > 0:
                    collided = True
                    break

        # проверяем столкновения с металлическими коробками
        if not collided:
            for obs_rect in metal_box.get_all_obstacle_rects():
                if self.rect_1.colliderect(obs_rect):
                    offset = (obs_rect.left - self.rect_1.left, obs_rect.top - self.rect_1.top)
                    if self.mask_1.overlap_area(metal_box.get_obstacle_mask(obs_rect), offset) > 0:
                        collided = True
                        break

        if collided:
            self.rect_1 = old_rect

    def move_2(self, dx=0, dy=0, wood_boxes=None, metal_boxes=None):
        if wood_boxes is None or metal_boxes is None:
            return

        old_rect = self.rect_2.copy()

        # попытка движения
        if (self.rect_2.left + dx * speed) > 0 and (self.rect_2.right + dx * speed) < W:
            self.rect_2.x += dx * speed
        if (self.rect_2.top + dy * speed) > 0 and (self.rect_2.bottom + dy * speed) < H:
            self.rect_2.y += dy * speed

        collided = False

        # используем первый элемент списков wood_boxes и metal_boxes
        wood_box = wood_boxes[0]
        metal_box = metal_boxes[0]

        # проверяем столкновения с деревянными коробками
        for obs_rect in wood_box.get_all_obstacle_rects():
            if self.rect_2.colliderect(obs_rect):
                offset = (obs_rect.left - self.rect_2.left, obs_rect.top - self.rect_2.top)
                if self.mask_2.overlap_area(wood_box.get_obstacle_mask(obs_rect), offset) > 0:
                    collided = True
                    break

        # проверяем столкновения с металлическими коробками
        if not collided:
            for obs_rect in metal_box.get_all_obstacle_rects():
                if self.rect_2.colliderect(obs_rect):
                    offset = (obs_rect.left - self.rect_2.left, obs_rect.top - self.rect_2.top)
                    if self.mask_2.overlap_area(metal_box.get_obstacle_mask(obs_rect), offset) > 0:
                        collided = True
                        break

        if collided:
            self.rect_2 = old_rect

    def draw(self, screen):
        self.cnt_iters += 1
        screen.blit(self.new_surf_1, self.rect_1)
        screen.blit(self.new_surf_2, self.rect_2)

    def can_shoot(self):
        return self.cnt_iters >= 40

    def shoot(self):
        self.cnt_iters = 0

    def get_mask1(self):
        return self.mask_1, self.rect_1

    def get_mask2(self):
        return self.mask_2, self.rect_2


class Bullet:
    def __init__(self, tank_rect, direction, tank_type=1):
        self.bullet_surf = pg.image.load('images/bullet.png').convert_alpha()
        self.bullet_surf = pg.transform.scale(self.bullet_surf,
                                              (self.bullet_surf.get_width() / 16,
                                               self.bullet_surf.get_height() / 16))

        # поворачиваем пулю в зависимости от того, как повернут танк
        if direction == 90:  # вправо
            self.bullet_surf = pg.transform.rotate(self.bullet_surf, -90)
        elif direction == 270:  # влево
            self.bullet_surf = pg.transform.rotate(self.bullet_surf, 90)
        elif direction == 180:  # вниз
            self.bullet_surf = pg.transform.rotate(self.bullet_surf, 180)

        if tank_type == 1:  # первый игрок
            if direction == 0:  # вверх
                self.bullet_rect = self.bullet_surf.get_rect(center=(tank_rect.centerx, tank_rect.top))
            elif direction == 90:  # вправо
                self.bullet_rect = self.bullet_surf.get_rect(center=(tank_rect.right, tank_rect.centery))
            elif direction == 180:  # вниз
                self.bullet_rect = self.bullet_surf.get_rect(center=(tank_rect.centerx, tank_rect.bottom))
            elif direction == 270:  # влево
                self.bullet_rect = self.bullet_surf.get_rect(center=(tank_rect.left, tank_rect.centery))
        else:  # второй игрок
            if direction == 0:  # вверх
                self.bullet_rect = self.bullet_surf.get_rect(center=(tank_rect.centerx, tank_rect.top))
            elif direction == 90:  # вправо
                self.bullet_rect = self.bullet_surf.get_rect(center=(tank_rect.right, tank_rect.centery))
            elif direction == 180:  # вниз
                self.bullet_rect = self.bullet_surf.get_rect(center=(tank_rect.centerx, tank_rect.bottom))
            elif direction == 270:  # влево
                self.bullet_rect = self.bullet_surf.get_rect(center=(tank_rect.left, tank_rect.centery))

        self.mask = pg.mask.from_surface(self.bullet_surf)
        self.direction = direction
        self.flag_active = True
        self.travel_distance = 0
        self.max_distance = 950

    def is_active(self):
        return self.flag_active

    def fly(self):
        if self.direction == 0:  # вверх
            self.bullet_rect.y -= bullet_speed
        elif self.direction == 90:  # вправо
            self.bullet_rect.x += bullet_speed
        elif self.direction == 180:  # вниз
            self.bullet_rect.y += bullet_speed
        elif self.direction == 270:  # влево
            self.bullet_rect.x -= bullet_speed

        if (self.bullet_rect.right < 0 or self.bullet_rect.left > W or
                self.bullet_rect.bottom < 0 or self.bullet_rect.top > H):
            self.flag_active = False

        self.travel_distance += bullet_speed
        if self.travel_distance >= self.max_distance:
            self.flag_active = False

    def draw(self, screen):
        screen.blit(self.bullet_surf, self.bullet_rect)


class HeartsDisplay:
    def __init__(self, tank_type="player1"):
        self.heart_image = pg.image.load('images/heart.png').convert_alpha()
        self.heart_image = pg.transform.scale(self.heart_image, (HEART_SIZE, HEART_SIZE))

        self.tank_type = tank_type
        self.lives = MAX_LIVES

        if tank_type == "player1":
            self.start_x = HEART_SPACING
        else:
            total_width = MAX_LIVES * HEART_SIZE + (MAX_LIVES - 1) * HEART_SPACING
            self.start_x = W - total_width - HEART_SPACING

        self.y = HEART_SPACING

    def draw(self, screen):
        for i in range(self.lives):
            x = self.start_x + i * (HEART_SIZE + HEART_SPACING)
            screen.blit(self.heart_image, (x, self.y))

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def is_alive(self):
        return self.lives > 0

    def reset(self):
        self.lives = MAX_LIVES


class WoodBoxes:
    def __init__(self):
        self.wood_surf = pg.image.load('images/wood_box.png')
        self.cur_wood_surf = pg.transform.scale(self.wood_surf,
                                                (self.wood_surf.get_width() / 10,
                                                 self.wood_surf.get_height() / 10))
        self.wood_size = self.wood_surf.get_width() / 10
        self.wood_surf = self.cur_wood_surf

        self.wood_positions = [
            (230, 0), (0, 260), (920, 660), (700, 920),
            (102, 840), (90 + self.wood_size * 2, 840), (765, 102), (778 - self.wood_size * 2, 102),
            (115, 515), (120 + self.wood_size - 11, 515), (107 + self.wood_size * 3 - 11, 515),
            (108 + self.wood_size * 4 - 17, 515),
            (550, 515 - self.wood_size + 8), (550 + self.wood_size - 8, 515 - self.wood_size + 8),
            (540 + self.wood_size * 3 - 8, 515 - self.wood_size + 8),
            (540 + self.wood_size * 4 - 13, 515 - self.wood_size + 8)
        ]
        self.cnt_wood_boxes = 16

        # создаем rect и маски блоков
        self.update_rects_and_masks()

    def update_rects_and_masks(self):
        self.wood_rects = [pg.Rect(x, y, self.wood_size, self.wood_size)
                           for x, y in self.wood_positions[:self.cnt_wood_boxes]]

        # маски для блоков (один раз для всех одинаковых блоков)
        self.wood_mask = pg.mask.from_surface(self.wood_surf)

    def get_all_obstacle_rects(self):
        return self.wood_rects

    def get_obstacle_mask(self, obs_rect):
        # obs_rect не используется, оставляем для совместимости
        return self.wood_mask

    def draw_wood_boxes(self, screen):
        for rect in self.wood_rects:
            screen.blit(self.wood_surf, rect)


class MetalBoxes:
    def __init__(self):
        self.wood_surf = pg.image.load('images/wood_box.png')

        self.metal_surf = pg.image.load('images/metal_box.png')
        self.cur_metal_surf = pg.transform.scale(self.metal_surf,
                                               (self.metal_surf.get_width() / 15,
                                                self.metal_surf.get_height() / 15))

        # используем wood_size из WoodBoxes для позиционирования
        self.wood_size = self.wood_surf.get_width() / 10
        self.metal_size = self.metal_surf.get_width() / 15
        self.metal_surf = self.cur_metal_surf

        self.metal_positions = [
            (233, self.wood_size - 3), (self.wood_size - 3, 263), (855, 663), (703, 855),
            (100 + self.wood_size, 835 + self.wood_size), (775 - self.wood_size, 111 - self.wood_size),
            (105 + self.wood_size * 2, 518), (117, 523 - self.wood_size),
            (96 + self.wood_size * 8, 526 - self.wood_size), (87 + self.wood_size * 10, 520)
        ]
        self.cnt_metal_boxes = 10

        # создаем rect и маски блоков
        self.update_rects_and_masks()

    def update_rects_and_masks(self):
        self.metal_rects = [pg.Rect(x, y, self.metal_size, self.metal_size)
                          for x, y in self.metal_positions[:self.cnt_metal_boxes]]

        # маски для блоков (один раз для всех одинаковых блоков)
        self.metal_mask = pg.mask.from_surface(self.metal_surf)

    def get_all_obstacle_rects(self):
        return self.metal_rects

    def get_obstacle_mask(self, obs_rect):
        # аргумент obs_rect не используется, но оставляем для совместимости
        return self.metal_mask

    def draw_metal_boxes(self, screen):
        for rect in self.metal_rects:
            screen.blit(self.metal_surf, rect)


class Tree:  # класс для куста. позволяет танку стать невидимым
    def __init__(self):
        self.tree_surf = pg.image.load("images/tree.png")
        self.tree_surf = pg.transform.scale(self.tree_surf,
                                            (self.tree_surf.get_width() / 6,
                                             self.tree_surf.get_height() / 6))
        self.tree_size = self.tree_surf.get_width() / 6
        self.wood_size = 740 / 10

        self.tree_positions = [
            (182, self.wood_size * 1.2), (self.wood_size * 1.45, 182), (656, 688), (695, 600),  # боковые кусты
            (40, 518 + self.wood_size * 1.2), (132 + self.tree_size, 518 + self.wood_size * 1.2),
            (250 + self.tree_size, 518 + self.wood_size * 1.2),  # левые центральные кусты
            (518 + self.wood_size * 3.3, 160), (518 + self.wood_size * 1.7, 160), (518, 160)
        ]
        self.cnt_trees = 10
        self.tree_rects = [pg.Rect(x, y, self.tree_size, self.tree_size)
                           for x, y in self.tree_positions[:self.cnt_trees]]

    def draw_trees(self, screen):
        for rect in self.tree_rects:
            screen.blit(self.tree_surf, rect)


def collisions_bullets_with_tanks(tank, bullets_player1, bullets_player2, player1_hearts, player2_hearts):
    # обработка пуль первого игрока (выстрелы первого танка)
    for bul_player1 in bullets_player1[:]:  # копия списка
        offset_1 = (bul_player1.bullet_rect.x - tank.rect_2.x, bul_player1.bullet_rect.y - tank.rect_2.y)

        if tank.mask_2.overlap(bul_player1.mask, offset_1) is not None:
            # попадание пули первого игрока в танк второго игрока
            player2_hearts.lose_life()
            bul_player1.flag_active = False  # деактивируем пулю после попадания
            bullets_player1.remove(bul_player1)  # удаляем пулю из списка
            tank_explode.play()
            return True  # возвращаем тру, чтобы показать, что было попадание

    # обработка пуль второго игрока (выстрелы второго танка)
    for bul_player2 in bullets_player2[:]:  # копия списка
        offset_2 = (bul_player2.bullet_rect.x - tank.rect_1.x, bul_player2.bullet_rect.y - tank.rect_1.y)

        if tank.mask_1.overlap(bul_player2.mask, offset_2) is not None:
            # попадание пули второго игрока в танк первого игрока
            player1_hearts.lose_life()
            bul_player2.flag_active = False  # деактивируем пулю после попадания
            bullets_player2.remove(bul_player2)  # удаляем пулю из списка
            tank_explode.play()
            return True  # возвращаем тру, чтобы показать, что было попадание

    return False


def collisions_bullets_with_blocks(bullets_player1, bullets_player2, wood_boxes, metal_boxes):
    # wood_boxes и metal_boxes - это списки объектов, берем первый (и единственный) элемент
    wood_box = wood_boxes[0]
    metal_box = metal_boxes[0]

    # обрабатываем пули первого игрока
    for bul_player1 in bullets_player1[:]:  # копия списка для безопасного удаления
        bullet_hit = False

        # проверяем столкновение с деревянными коробками
        for w_rect in wood_box.wood_rects[:]:  # копия для безопасного удаления
            if bul_player1.bullet_rect.colliderect(w_rect):
                offset = (w_rect.left - bul_player1.bullet_rect.left,
                          w_rect.top - bul_player1.bullet_rect.top)
                if wood_box.wood_mask.overlap(bul_player1.mask, offset):
                    bullet_hit = True
                    # удаляем деревянную коробку при попадании
                    if w_rect in wood_box.wood_rects:
                        wood_box.wood_rects.remove(w_rect)
                        wood_box.cnt_wood_boxes -= 1
                        wood_broke.play()
                    break

        # проверяем столкновение с металлическими коробками (не удаляем их)
        if not bullet_hit:
            for m_rect in metal_box.metal_rects:
                if bul_player1.bullet_rect.colliderect(m_rect):
                    offset = (m_rect.left - bul_player1.bullet_rect.left,
                              m_rect.top - bul_player1.bullet_rect.top)
                    if metal_box.metal_mask.overlap(bul_player1.mask, offset):
                        bullet_hit = True
                        metal_strike.play()
                        break

        # если пуля попала в коробку, деактивируем ее
        if bullet_hit:
            bul_player1.flag_active = False

    # обрабатываем пули второго игрока
    for bul_player2 in bullets_player2[:]:  # копия списка для безопасного удаления
        bullet_hit = False

        # проверяем столкновение с деревянными коробками
        for w_rect in wood_box.wood_rects[:]:  # копия для безопасного удаления
            if bul_player2.bullet_rect.colliderect(w_rect):
                offset = (w_rect.left - bul_player2.bullet_rect.left,
                          w_rect.top - bul_player2.bullet_rect.top)
                if wood_box.wood_mask.overlap(bul_player2.mask, offset):
                    bullet_hit = True
                    # удаляем деревянную коробку при попадании
                    if w_rect in wood_box.wood_rects:
                        wood_box.wood_rects.remove(w_rect)
                        wood_box.cnt_wood_boxes -= 1
                        wood_broke.play()
                    break

        # проверяем столкновение с металлическими коробки (не удаляем их)
        if not bullet_hit:
            for m_rect in metal_box.metal_rects:
                if bul_player2.bullet_rect.colliderect(m_rect):
                    offset = (m_rect.left - bul_player2.bullet_rect.left,
                              m_rect.top - bul_player2.bullet_rect.top)
                    if metal_box.metal_mask.overlap(bul_player2.mask, offset):
                        bullet_hit = True
                        metal_strike.play()
                        break

        # если пуля попала в коробку, деактивируем ее
        if bullet_hit:
            bul_player2.flag_active = False


def show_start_screen():
    waiting = True
    while waiting:
        screen.blit(background_image, (0, 0))

        overlay = pg.Surface((W, H), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title_font = pg.font.Font(None, 72)
        title_text = title_font.render('ТАНКИ', True, (255, 255, 0))
        screen.blit(title_text, (W // 2 - title_text.get_width() // 2, H // 4))

        font = pg.font.Font(None, 45)
        start_text_player1_1 = font.render('Управление для первого игрока:', True, (100, 200, 255))
        start_text_player1_2 = font.render('WASD, стрельба - ПРОБЕЛ', True, (100, 200, 255))
        start_text_player2_1 = font.render('Управление для второго игрока:', True,(255, 100, 100))
        start_text_player2_2 = font.render('стрелки, стрельба - правый CTRL', True,(255, 100, 100))

        # позиционируем текст
        screen.blit(start_text_player1_1, (W // 3.8 - start_text_player1_1.get_width() // 2, H // 2.6))
        screen.blit(start_text_player1_2, (W // 4 - start_text_player1_2.get_width() // 2, H // 2.3))
        screen.blit(start_text_player2_1, (W // 1.4 - start_text_player2_1.get_width() // 2, H // 1.87))
        screen.blit(start_text_player2_2, (W // 1.4 - start_text_player2_2.get_width() // 2, H // 1.7))

        start_info = font.render('Нажмите любую клавишу для начала игры', True, (255, 255, 255))
        screen.blit(start_info, (W // 2 - start_info.get_width() // 2, H * 3 // 4))

        pg.display.update()

        # обработка событий в стартовом экране
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                waiting = False


def show_screen_for_choose_skins():  # функция для выбора скинов танков
    global waiting_for_choose, tank, player1_skin, player2_skin

    # инициализируем переменные для хранения выбранных скинов
    player1_skin = 'images/blue_tank.png'  # скин по умолчанию для 1-го игрока
    player2_skin = 'images/red_tank.png'  # скин по умолчанию для 2-го игрока

    selected_tank1_rect = None
    selected_tank2_rect = None

    # рамка
    frame_surf = pg.image.load('images/blue_frame.png').convert_alpha()
    frame_surf = pg.transform.scale(frame_surf,
                                         (frame_surf.get_width() / 7, frame_surf.get_height() / 6))
    player1_frame_rect = frame_surf.get_rect(center=(W / 12, H / 3))

    # загружаем и масштабируем изображения танков
    green_surf = pg.image.load('images/green_tank.png').convert_alpha()
    green_surf = pg.transform.scale(green_surf, (green_surf.get_width() / 8, green_surf.get_height() / 8))

    purple_surf = pg.image.load('images/purple_tank.png').convert_alpha()
    purple_surf = pg.transform.scale(purple_surf, (purple_surf.get_width() / 8, purple_surf.get_height() / 8))

    orange_surf = pg.image.load('images/orange_tank.png').convert_alpha()
    orange_surf = pg.transform.scale(orange_surf, (orange_surf.get_width() / 8, orange_surf.get_height() / 8))

    blue_surf = pg.image.load('images/blue_tank.png').convert_alpha()
    blue_surf = pg.transform.scale(blue_surf, (blue_surf.get_width() / 8, blue_surf.get_height() / 8))

    red_surf = pg.image.load('images/red_tank.png').convert_alpha()
    red_surf = pg.transform.scale(red_surf, (red_surf.get_width() / 8, red_surf.get_height() / 8))

    # создаем прямоугольники для первого игрока (верхний ряд)
    green_rect_1 = green_surf.get_rect(center=(W / 4.7, H / 3))
    purple_rect_1 = purple_surf.get_rect(center=(W / 2.87, H / 3))
    orange_rect_1 = orange_surf.get_rect(center=(W / 2.07, H / 3))
    blue_rect_1 = blue_surf.get_rect(center=(W / 1.6, H / 3))
    red_rect_1 = red_surf.get_rect(center=(W / 1.3, H / 3))

    # создаем прямоугольники для второго игрока (нижний ряд)
    green_rect_2 = green_surf.get_rect(center=(W / 4.7, H * 3 / 4))
    purple_rect_2 = purple_surf.get_rect(center=(W / 2.87, H * 3 / 4))
    orange_rect_2 = orange_surf.get_rect(center=(W / 2.07, H * 3 / 4))
    blue_rect_2 = blue_surf.get_rect(center=(W / 1.6, H * 3 / 4))
    red_rect_2 = red_surf.get_rect(center=(W / 1.3, H * 3 / 4))

    frame_surf = pg.image.load('images/blue_frame.png').convert_alpha()
    frame_surf = pg.transform.scale(frame_surf,
                                         (frame_surf.get_width() / 7, frame_surf.get_height() / 6))

    font = pg.font.Font(None, 45)
    players_font = pg.font.Font(None, 45)

    while waiting_for_choose:
        screen.blit(background_image, (0, 0))

        overlay = pg.Surface((W, H), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # заголовок
        title_font = pg.font.Font(None, 72)
        title_text = title_font.render('ВЫБЕРИТЕ СКИНЫ', True, (255, 255, 0))
        screen.blit(title_text, (W // 2 - title_text.get_width() // 2, H // 10))

        players_text_1 = players_font.render('Первый игрок:', True, (255, 255, 255))
        screen.blit(players_text_1, (W // 2.9, H // 4.6))

        players_text_2 = players_font.render('Второй игрок:', True, (255, 255, 255))
        screen.blit(players_text_2, (W // 2.9, H // 1.55))

        # отрисовка скинов для 1-го игрока (верхний ряд)
        screen.blit(green_surf, green_rect_1)
        screen.blit(purple_surf, purple_rect_1)
        screen.blit(orange_surf, orange_rect_1)
        screen.blit(blue_surf, blue_rect_1)
        screen.blit(red_surf, red_rect_1)

        # отрисовка скинов для 2-го игрока (нижний ряд)
        screen.blit(green_surf, green_rect_2)
        screen.blit(purple_surf, purple_rect_2)
        screen.blit(orange_surf, orange_rect_2)
        screen.blit(blue_surf, blue_rect_2)
        screen.blit(red_surf, red_rect_2)

        if selected_tank1_rect:
            frame_rect = frame_surf.get_rect(center=selected_tank1_rect.center)
            screen.blit(frame_surf, frame_rect)

        if selected_tank2_rect:
            frame_rect = frame_surf.get_rect(center=selected_tank2_rect.center)
            screen.blit(frame_surf, frame_rect)

        # инструкция
        start_info = font.render('Нажмите любую клавишу для продолжения...', True, (255, 255, 255))
        screen.blit(start_info, (W // 2 - start_info.get_width() // 2, H - 100))

        pg.display.update()

        # обработка событий в стартовом экране
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # проверка выбора для первого игрока (верхний ряд)
                if green_rect_1.collidepoint(mouse_pos):
                    if player2_skin != 'images/green_tank.png':  # проверяем, не выбран ли уже этот танк вторым игроком
                        player1_skin = 'images/green_tank.png'
                        selected_tank1_rect = green_rect_1
                elif purple_rect_1.collidepoint(mouse_pos):
                    if player2_skin != 'images/purple_tank.png':
                        player1_skin = 'images/purple_tank.png'
                        selected_tank1_rect = purple_rect_1
                elif orange_rect_1.collidepoint(mouse_pos):
                    if player2_skin != 'images/orange_tank.png':
                        player1_skin = 'images/orange_tank.png'
                        selected_tank1_rect = orange_rect_1
                elif blue_rect_1.collidepoint(mouse_pos):
                    if player2_skin != 'images/blue_tank.png':
                        player1_skin = 'images/blue_tank.png'
                        selected_tank1_rect = blue_rect_1
                elif red_rect_1.collidepoint(mouse_pos):
                    if player2_skin != 'images/red_tank.png':
                        player1_skin = 'images/red_tank.png'
                        selected_tank1_rect = red_rect_1

                # проверка выбора для второго игрока (нижний ряд)
                elif green_rect_2.collidepoint(mouse_pos):
                    if player1_skin != 'images/green_tank.png':  # проверяем, не выбран ли уже этот танк первым игроком
                        player2_skin = 'images/green_tank.png'
                        selected_tank2_rect = green_rect_2
                elif purple_rect_2.collidepoint(mouse_pos):
                    if player1_skin != 'images/purple_tank.png':
                        player2_skin = 'images/purple_tank.png'
                        selected_tank2_rect = purple_rect_2
                elif orange_rect_2.collidepoint(mouse_pos):
                    if player1_skin != 'images/orange_tank.png':
                        player2_skin = 'images/orange_tank.png'
                        selected_tank2_rect = orange_rect_2
                elif blue_rect_2.collidepoint(mouse_pos):
                    if player1_skin != 'images/blue_tank.png':
                        player2_skin = 'images/blue_tank.png'
                        selected_tank2_rect = blue_rect_2
                elif red_rect_2.collidepoint(mouse_pos):
                    if player1_skin != 'images/red_tank.png':
                        player2_skin = 'images/red_tank.png'
                        selected_tank2_rect = red_rect_2

            if event.type == pg.KEYDOWN:
                waiting_for_choose = False

    # создаем танк с выбранными скинами
    tank = Tank(player1_skin, player2_skin)


pg.init()

wood_broke = pg.mixer.Sound('sounds/wood_broke.wav')
metal_strike = pg.mixer.Sound('sounds/strike_metal.wav')
tank_explode = pg.mixer.Sound('sounds/tank_explode.wav')
shot = pg.mixer.Sound('sounds/tank_shot.wav')
pg.mixer.music.load('sounds/tank_music_backgr.wav')
pg.mixer.music.play(-1)
screen = pg.display.set_mode((W, H))
pg.display.set_caption("Tanks")
clock = pg.time.Clock()

tank = Tank(None, None)
background_image = pg.image.load('images/background.jpg').convert()
background_image = pg.transform.scale(background_image, (W, H))
win_font = pg.font.Font(None, 36)
show_screen_for_choose_skins()

if not waiting_for_choose:
    show_start_screen()

player1_hearts = HeartsDisplay("player1")
player2_hearts = HeartsDisplay("player2")

wood_boxes = [WoodBoxes()]
metal_boxes = [MetalBoxes()]
trees = [Tree()]

bullets_player1 = []
bullets_player2 = []

game_over = False
winner = ''
flag_play = True


def reset_game():
    """Сброс игры до начального состояния"""
    global tank, player1_hearts, player2_hearts, wood_boxes, metal_boxes, bullets_player1, bullets_player2, game_over, winner

    tank = Tank(player1_skin, player2_skin)
    player1_hearts.reset()
    player2_hearts.reset()

    # создаем новые объекты коробок вместо очистки списков
    wood_boxes = [WoodBoxes()]
    metal_boxes = [MetalBoxes()]

    bullets_player1.clear()
    bullets_player2.clear()
    game_over = False
    winner = ""


while flag_play:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            flag_play = False
            break
        if event.type == pg.KEYDOWN and game_over:
            if event.key == pg.K_r:  # Рестарт игры
                reset_game()

    if not flag_play:
        break

    if not game_over:
        keys = pg.key.get_pressed()

        # прописываем движение и выстрел для 1-го игрока
        if keys[pg.K_a]:
            tank.rect_1 = tank.flip2_player1()
            tank.move_1(dx=-1, wood_boxes=wood_boxes, metal_boxes=metal_boxes)
        elif keys[pg.K_d]:
            tank.rect_1 = tank.flip1_player1()
            tank.move_1(dx=1, wood_boxes=wood_boxes, metal_boxes=metal_boxes)
        elif keys[pg.K_w]:
            tank.rect_1 = tank.flip3_player1()
            tank.move_1(dy=-1, wood_boxes=wood_boxes, metal_boxes=metal_boxes)
        elif keys[pg.K_s]:
            tank.rect_1 = tank.flip4_player1()
            tank.move_1(dy=1, wood_boxes=wood_boxes, metal_boxes=metal_boxes)

        if keys[pg.K_SPACE] and tank.can_shoot():
            tank.shoot()
            bullets_player1.append(Bullet(tank.rect_1, tank.direction_1, 1))
            shot.play()  # проигрываем звук выстрела

        # прописываем движение и выстрел для 2-го игрока
        if keys[pg.K_LEFT]:
            tank.rect_2 = tank.flip2_player2()
            tank.move_2(dx=-1, wood_boxes=wood_boxes, metal_boxes=metal_boxes)
        elif keys[pg.K_RIGHT]:
            tank.rect_2 = tank.flip1_player2()
            tank.move_2(dx=1, wood_boxes=wood_boxes, metal_boxes=metal_boxes)
        elif keys[pg.K_UP]:
            tank.rect_2 = tank.flip3_player2()
            tank.move_2(dy=-1, wood_boxes=wood_boxes, metal_boxes=metal_boxes)
        elif keys[pg.K_DOWN]:
            tank.rect_2 = tank.flip4_player2()
            tank.move_2(dy=1, wood_boxes=wood_boxes, metal_boxes=metal_boxes)

        if keys[pg.K_RCTRL] and tank.can_shoot():
            tank.shoot()
            bullets_player2.append(Bullet(tank.rect_2, tank.direction_2, 2))
            shot.play()  # проигрываем звук выстрела

        # проверка столкновений пуль с танками
        collisions_bullets_with_tanks(tank, bullets_player1, bullets_player2, player1_hearts, player2_hearts)

        # проверка столкновений пуль с блоками
        collisions_bullets_with_blocks(bullets_player1, bullets_player2, wood_boxes, metal_boxes)

    screen.blit(background_image, (0, 0))

    # отрисовываем все коробки
    for w_box in wood_boxes:
        w_box.draw_wood_boxes(screen)
    for m_box in metal_boxes:
        m_box.draw_metal_boxes(screen)

    # отрисовка сердец и танков
    player1_hearts.draw(screen)
    player2_hearts.draw(screen)
    tank.draw(screen)

    # отрисовываем все пули
    for bullet in bullets_player1:
        bullet.fly()
        bullet.draw(screen)

    for bullet in bullets_player2:
        bullet.fly()
        bullet.draw(screen)

    # отрисовка кустов
    for tree in trees:
        tree.draw_trees(screen)

    bullets_player1 = [bullet for bullet in bullets_player1 if bullet.is_active()]
    bullets_player2 = [bullet for bullet in bullets_player2 if bullet.is_active()]

    if not game_over:
        if not player1_hearts.is_alive():
            game_over = True
            winner = "Второй игрок"
        elif not player2_hearts.is_alive():
            game_over = True
            winner = "Первый игрок"

    # отображаем экран конца игры
    if game_over:
        overlay = pg.Surface((W, H), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # отображаем победителя
        winner_text = win_font.render(f"Победитель: {winner}!", True, (255, 255, 255))
        restart_text = win_font.render("Нажмите R для рестарта", True, (255, 255, 255))

        screen.blit(winner_text, (W // 2 - winner_text.get_width() // 2, H // 2 - 50))
        screen.blit(restart_text, (W // 2 - restart_text.get_width() // 2, H // 2 + 20))

    pg.display.update()

pg.quit()
