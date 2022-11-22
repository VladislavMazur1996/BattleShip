from random import randrange


class BoardOutException(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'{(self.x, self.y)}'


class Ship:
    def __init__(self, length, bow, route):
        self.length = length
        self.bow = bow
        self.route = route
        self.life = length

    def dots(self):
        dots = []
        for index in range(self.length):
            if self.route:
                dots.append(Dot(self.bow.x, self.bow.y + index))
            else:
                dots.append(Dot(self.bow.x + index, self.bow.y))
        return dots


class Board:
    def __init__(self, hid=False):
        self.board = [['0' for _ in range(6)] for _ in range(6)]
        self.ships = []
        self.busy = []
        self.hid = hid

    def add_ship(self, ship):
        for dot in ship.dots():
            if not (0 <= dot.x < 6 and 0 <= dot.y < 6) or dot in self.busy:
                return False
        for dot in ship.dots():
            self.board[dot.x][dot.y] = '■'
        self.contour(ship)
        self.ships.append(ship)
        return True

    def contour(self, ship, sink=False):
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1), (0, 0), (0, 1),
                   (1, -1), (1, 0), (1, 1)]
        for dot in ship.dots():
            for i, q in offsets:
                if 0 <= dot.x + i < 6 and 0 <= dot.y + q < 6 and sink:
                    if self.board[dot.x + i][dot.y + q] != 'X':
                        self.board[dot.x + i][dot.y + q] = '.'
                elif 0 <= dot.x + i < 6 and 0 <= dot.y + q < 6:
                    self.busy.append(Dot(dot.x + i, dot.y + q))

    def shot(self, dot):
        if str(self.board[dot.x][dot.y]) in 'TX.':
            print('В данное поле уже был выстрел.')
            return True
        if self.board[dot.x][dot.y] == '■':
            self.board[dot.x][dot.y] = 'X'
            for ship in self.ships:
                if dot in ship.dots():
                    if ship.life > 1:
                        ship.life -= 1
                        print('Корабль подбит!')
                    else:
                        print('Корабль убит!')
                        self.sink(ship)
            return True
        elif self.board[dot.x][dot.y] == '0':
            self.board[dot.x][dot.y] = 'T'
            return False

    def sink(self, ship):
        self.contour(ship, True)
        self.ships.remove(ship)

    def __str__(self):
        res = "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.board):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "O")
        return res


class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        if self.enemy_board.shot(self.ask()):
            return True
        return False


class AI(Player):
    def ask(self):
        return Dot(randrange(0, 6), randrange(0, 6))


class User(Player):
    def ask(self):
        while True:
            try:
                x, y = map(lambda x: int(x) - 1, input().split())
                if 0 <= x < 6 and 0 <= y < 6:
                    return Dot(x, y)
                else:
                    raise BoardOutException
            except ValueError:
                print('Ошибка ввода')
            except BoardOutException:
                print('Выстрел за границы карты!!!')


class Game:
    def __init__(self):
        self.player_board = self.random_board(Board())
        self.ai_board = self.random_board(Board(True))
        self.player = User(self.player_board, self.ai_board)
        self.ai = AI(self.ai_board, self.player_board)

    def random_board(self, board):
        ships = [3, 2, 2, 1, 1, 1, 1]
        for _ in range(10**4):
            ship = Ship(ships[0], Dot(randrange(0, 7), randrange(0, 7)), randrange(0, 2))
            if board.add_ship(ship):
                ships.pop(0)
            if ships:
                continue
            else:
                return board
        return self.random_board(Board(board.hid))

    def greet(self):
        print("-" * 20)
        print("  Приветствуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-" * 20)
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        flag = True
        while self.ai_board.ships and self.player_board.ships:
            print('Карта игрока:')
            print(self.player_board)
            print("-" * 20)
            print('Карта противника:')
            print(self.ai_board)
            print("-" * 20)
            if flag:
                print('Ход игрока:')
                flag = True if self.player.move() else False
            else:
                flag = False if self.ai.move() else True
        else:
            if self.ai_board.ships:
                print('Вы проиграли.')
            else:
                print('Поздравляю, вы выиграли!!!')

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
