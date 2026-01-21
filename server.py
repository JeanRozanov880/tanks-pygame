import socket
import pickle
import threading
import pygame as pg

# Конфигурация сети
HOST = '0.0.0.0'  # Все доступные интерфейсы
PORT = 5555

# Константы игры
FPS = 60
W, H = 1000, 1000
BG = (100, 170, 220)
speed = 3
bullet_speed = 6
HEART_SIZE = 40
MAX_LIVES = 3
HEART_SPACING = 10

class GameServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen(2)
        print(f"Сервер запущен на {HOST}:{PORT}")

        self.players = []
        self.current_player = 0
        self.game_state = {
            'blue_tank': {'x': W / 12, 'y': H / 7, 'direction': 0, 'lives': MAX_LIVES},
            'red_tank': {'x': W / 1.1, 'y': H / 1.1, 'direction': 0, 'lives': MAX_LIVES},
            'bullets_blue': [],
            'bullets_red': [],
            'wood_boxes': [],
            'bet_boxes': [],
            'game_over': False,
            'winner': ''
        }

        # Инициализация Pygame для обработки ввода
        pg.init()
        self.screen = pg.display.set_mode((1, 1))
        self.clock = pg.time.Clock()

    def handle_client(self, conn, addr, player_id):
        print(f"Игрок {player_id} подключился: {addr}")

        try:
            # Отправляем игроку его ID
            conn.send(str(player_id).encode())

            while True:
                # Получаем данные от клиента
                try:
                    data = conn.recv(4096)
                    if not data:
                        break

                    player_input = pickle.loads(data)

                    # Обновляем состояние игры на основе ввода игрока
                    self.update_game_state(player_id, player_input)

                    # Отправляем обновленное состояние всем игрокам
                    self.broadcast_game_state()

                except Exception as e:
                    print(f"Ошибка при обработке данных от игрока {player_id}: {e}")
                    break

        except Exception as e:
            print(f"Ошибка соединения с игроком {player_id}: {e}")
        finally:
            print(f"Игрок {player_id} отключился")
            if conn in self.players:
                self.players.remove(conn)
            conn.close()

    def update_game_state(self, player_id, player_input):
        # Здесь будет логика обновления игры
        # Для простоты сразу обновляем позиции танков
        if player_id == 0:  # Синий танк
            if 'pos' in player_input:
                self.game_state['blue_tank'].update(player_input['pos'])
            if 'bullet' in player_input:
                self.game_state['bullets_blue'].append(player_input['bullet'])
        else:  # Красный танк
            if 'pos' in player_input:
                self.game_state['red_tank'].update(player_input['pos'])
            if 'bullet' in player_input:
                self.game_state['bullets_red'].append(player_input['bullet'])

        if 'lives' in player_input:
            tank = 'blue_tank' if player_id == 0 else 'red_tank'
            self.game_state[tank]['lives'] = player_input['lives']

        if 'game_over' in player_input:
            self.game_state['game_over'] = player_input['game_over']
            self.game_state['winner'] = player_input['winner']

    def broadcast_game_state(self):
        game_state_data = pickle.dumps(self.game_state)
        for player in self.players:
            try:
                player.send(game_state_data)
            except:
                pass

    def run(self):
        print("Ожидание подключения игроков...")

        # Принимаем двух игроков
        while len(self.players) < 2:
            conn, addr = self.server.accept()
            self.players.append(conn)

            # Создаем поток для обработки клиента
            thread = threading.Thread(target=self.handle_client, args=(conn, addr, len(self.players)-1))
            thread.daemon = True
            thread.start()

        print("Оба игрока подключены! Игра начинается...")

        # Главный игровой цикл сервера
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # Проверяем, оба ли игрока на месте
            if len(self.players) < 2:
                print("Один из игроков отключился. Ожидание переподключения...")
                # Здесь можно добавить логику переподключения

        self.server.close()

if __name__ == "__main__":
    server = GameServer()
    server.run()
