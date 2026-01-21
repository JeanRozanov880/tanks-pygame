import socket
import pickle
import threading
import pygame as pg

# Настройки подключения
SERVER_HOST = input("Введите IP адрес сервера: ") or 'localhost'
SERVER_PORT = 5555

# Константы игры (такие же как на сервере)
FPS = 60
W, H = 1000, 1000
BG = (100, 170, 220)
speed = 3
bullet_speed = 6
HEART_SIZE = 40
MAX_LIVES = 3
HEART_SPACING = 10

class TankGameClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player_id = None
        self.game_state = None
        self.local_state = {}  # Локальное состояние для сглаживания

        # Инициализация Pygame
        pg.init()
        pg.mixer.init()

        # Загрузка звуков
        self.wood_broke = pg.mixer.Sound('sounds/wood_broke.wav')
        self.metal_strike = pg.mixer.Sound('sounds/strike_metal.wav')
        self.tank_explode = pg.mixer.Sound('sounds/tank_explode.wav')
        self.shot = pg.mixer.Sound('sounds/tank_shot.wav')

        # Создание экрана
        self.screen = pg.display.set_mode((W, H))
        pg.display.set_caption("Tanks Online")

        # Загрузка ресурсов
        self.load_resources()

        # Таймер для отправки данных
        self.last_send_time = 0
        self.send_interval = 0.05  # Отправлять данные каждые 50мс

    def load_resources(self):
        """Загрузка всех графических ресурсов"""
        # Фон
        self.background_image = pg.image.load('images/background.jpg').convert()
        self.background_image = pg.transform.scale(self.background_image, (W, H))

        # Танки
        self.blue_tank_img = pg.image.load('images/blue_tank.png').convert_alpha()
        self.blue_tank_img = pg.transform.scale(self.blue_tank_img,
                                                (self.blue_tank_img.get_width() / 8,
                                                 self.blue_tank_img.get_height() / 8))

        self.red_tank_img = pg.image.load('images/red_tank.png').convert_alpha()
        self.red_tank_img = pg.transform.scale(self.red_tank_img,
                                               (self.red_tank_img.get_width() / 8,
                                                self.red_tank_img.get_height() / 8))

        # Пуля
        self.bullet_img = pg.image.load('images/bullet.png').convert_alpha()
        self.bullet_img = pg.transform.scale(self.bullet_img,
                                             (self.bullet_img.get_width() / 16,
                                              self.bullet_img.get_height() / 16))

        # Сердца
        self.heart_img = pg.image.load('images/heart.png').convert_alpha()
        self.heart_img = pg.transform.scale(self.heart_img, (HEART_SIZE, HEART_SIZE))

        # Блоки
        self.wood_box_img = pg.image.load('images/wood_box.png')
        self.wood_box_img = pg.transform.scale(self.wood_box_img,
                                               (self.wood_box_img.get_width() / 10,
                                                self.wood_box_img.get_height() / 10))

        self.bet_box_img = pg.image.load('images/beton_box.png')
        self.bet_box_img = pg.transform.scale(self.bet_box_img,
                                              (self.bet_box_img.get_width() / 15,
                                               self.bet_box_img.get_height() / 15))

        # Кусты
        self.tree_img = pg.image.load('images/tree.png')
        self.tree_img = pg.transform.scale(self.tree_img,
                                           (self.tree_img.get_width() / 6,
                                            self.tree_img.get_height() / 6))

        # Шрифт
        self.font = pg.font.Font(None, 36)

    def connect_to_server(self):
        """Подключение к серверу"""
        try:
            self.client.connect((SERVER_HOST, SERVER_PORT))
            # Получаем ID игрока
            self.player_id = int(self.client.recv(1024).decode())
            print(f"Подключен к серверу как игрок {self.player_id}")
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def receive_data(self):
        """Получение данных от сервера в отдельном потоке"""
        while True:
            try:
                data = self.client.recv(4096)
                if not data:
                    break

                # Десериализуем состояние игры
                self.game_state = pickle.loads(data)

            except Exception as e:
                print(f"Ошибка при получении данных: {e}")
                break

    def send_input(self, player_input):
        """Отправка ввода игрока на сервер"""
        try:
            data = pickle.dumps(player_input)
            self.client.send(data)
        except Exception as e:
            print(f"Ошибка при отправке данных: {e}")

    def draw_tank(self, tank_data, is_blue=True):
        """Отрисовка танка"""
        if not tank_data:
            return

        # Получаем изображение танка
        tank_img = self.blue_tank_img if is_blue else self.red_tank_img

        # Поворачиваем изображение в зависимости от направления
        direction = tank_data.get('direction', 0)
        rotated_img = pg.transform.rotate(tank_img, -direction)

        # Получаем позицию
        x = tank_data.get('x', 0)
        y = tank_data.get('y', 0)

        # Рисуем танк
        rect = rotated_img.get_rect(center=(x, y))
        self.screen.blit(rotated_img, rect)

        # Рисуем жизни
        lives = tank_data.get('lives', MAX_LIVES)
        self.draw_hearts(lives, is_blue)

    def draw_hearts(self, lives, is_blue=True):
        """Отрисовка сердечек (жизней)"""
        for i in range(lives):
            if is_blue:
                x = HEART_SPACING + i * (HEART_SIZE + HEART_SPACING)
            else:
                total_width = MAX_LIVES * HEART_SIZE + (MAX_LIVES - 1) * HEART_SPACING
                x = W - total_width - HEART_SPACING + i * (HEART_SIZE + HEART_SPACING)

            y = HEART_SPACING
            self.screen.blit(self.heart_img, (x, y))

    def draw_bullets(self, bullets_data, color='blue'):
        """Отрисовка пуль"""
        for bullet in bullets_data:
            x = bullet.get('x', 0)
            y = bullet.get('y', 0)
            direction = bullet.get('direction', 0)

            # Поворачиваем пулю
            rotated_bullet = pg.transform.rotate(self.bullet_img, -direction)
            rect = rotated_bullet.get_rect(center=(x, y))
            self.screen.blit(rotated_bullet, rect)

    def run(self):
        """Главный игровой цикл"""
        if not self.connect_to_server():
            return

        # Запускаем поток для получения данных
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.daemon = True
        receive_thread.start()

        clock = pg.time.Clock()
        running = True

        # Локальное состояние управления
        keys_pressed = {
            'up': False, 'down': False, 'left': False, 'right': False, 'shoot': False
        }

        last_shoot_time = 0
        shoot_cooldown = 500  # 0.5 секунды между выстрелами

        while running:
            current_time = pg.time.get_ticks()
            clock.tick(FPS)

            # Обработка событий
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_r and self.game_state and self.game_state.get('game_over', False):
                        # Отправка запроса на рестарт
                        self.send_input({'restart': True})

            # Получаем состояние клавиш
            keys = pg.key.get_pressed()

            # В зависимости от ID игрока определяем управление
            if self.player_id == 0:  # Синий танк (WASD + Space)
                keys_pressed['up'] = keys[pg.K_w]
                keys_pressed['down'] = keys[pg.K_s]
                keys_pressed['left'] = keys[pg.K_a]
                keys_pressed['right'] = keys[pg.K_d]
                keys_pressed['shoot'] = keys[pg.K_SPACE]
            else:  # Красный танк (Стрелки + Enter)
                keys_pressed['up'] = keys[pg.K_UP]
                keys_pressed['down'] = keys[pg.K_DOWN]
                keys_pressed['left'] = keys[pg.K_LEFT]
                keys_pressed['right'] = keys[pg.K_RIGHT]
                keys_pressed['shoot'] = keys[pg.K_RETURN] or keys[pg.K_KP_ENTER]

            # Отправляем ввод на сервер
            player_input = {'keys': keys_pressed.copy()}

            # Обработка выстрела
            if keys_pressed['shoot'] and current_time - last_shoot_time > shoot_cooldown:
                player_input['shoot'] = True
                last_shoot_time = current_time
                self.shot.play()

            # Отправляем данные с интервалом
            if current_time - self.last_send_time > self.send_interval * 1000:
                self.send_input(player_input)
                self.last_send_time = current_time

            # Отрисовка
            self.screen.blit(self.background_image, (0, 0))

            # Рисуем игровые объекты если есть состояние от сервера
            if self.game_state:
                # Рисуем танки
                self.draw_tank(self.game_state.get('blue_tank'), is_blue=True)
                self.draw_tank(self.game_state.get('red_tank'), is_blue=False)

                # Рисуем пули
                self.draw_bullets(self.game_state.get('bullets_blue', []), 'blue')
                self.draw_bullets(self.game_state.get('bullets_red', []), 'red')

                # Проверяем конец игры
                if self.game_state.get('game_over', False):
                    self.draw_game_over()

            pg.display.flip()

        self.client.close()
        pg.quit()

    def draw_game_over(self):
        """Отрисовка экрана окончания игры"""
        overlay = pg.Surface((W, H), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        winner = self.game_state.get('winner', '')
        winner_text = self.font.render(f"Победитель: {winner}!", True, (255, 255, 255))
        restart_text = self.font.render("Нажмите R для рестарта", True, (255, 255, 255))

        self.screen.blit(winner_text, (W // 2 - winner_text.get_width() // 2, H // 2 - 50))
        self.screen.blit(restart_text, (W // 2 - restart_text.get_width() // 2, H // 2 + 20))

if __name__ == "__main__":
    game = TankGameClient()
    game.run()
