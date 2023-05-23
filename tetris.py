import pygame
import random

# Цвета для кубиков
colors = [
    (0, 0, 0),       # чёрный
    (120, 37, 179),  # фиолетовый
    (100, 179, 179), # голубой
    (255, 51, 0),    # красный
    (135, 233, 38),  # зелёный
    (253, 228, 66),  # жёлтый
    (180, 34, 122),  # розовый
]

"""Класс для фигуры, ее параметры"""
class Figure:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7 ], [1, 5, 9, 13 ], [4, 5, 6, 7 ]], # I
        [[4, 5, 9, 10], [2, 6, 5, 9 ], [4, 5, 9, 10 ], [2, 6, 5, 9 ]], # Z
        [[6, 7, 9, 10], [1, 5, 6, 10], [6, 7, 9, 10 ], [1, 5, 6, 10]], # S
        [[1, 2, 5, 9 ], [4, 5, 6, 10], [1, 5, 9, 8  ], [0, 4, 5, 6 ]], # j
        [[1, 2, 6, 10], [3, 5, 6, 7 ], [2, 6, 10, 11], [5, 6, 7, 9 ]], # L
        [[1, 4, 5, 6 ], [1, 5, 6, 9 ], [4, 5, 6, 9  ] ,[1, 4, 5, 9 ]], # T
        [[1, 2, 5, 6 ], [1, 2, 5, 6 ], [1, 2, 5, 6  ], [1, 2, 5, 6 ]], # Куб
        [[9],[9],[9],[9]], #кубик
        [[5,9],[9,10],[5,9],[9,10]], #два кубика
        [[5,9,10],[5,6,10],[6,10,9],[5,9,10]] #ступенька
    ]

    #создаём фигуру
    def __init__(self, x, y):
        self.x = x # положение фигуры на поле
        self.y = y # положение фигуры на поле

        self.type  = random.randint(0, len(self.figures) - 1) #тип фигуры
        self.color = random.randint(1, len(colors) - 1)       #цвет фигуры
        self.rotation = 0 #поворот фигуры

    #Возвращает массив с позициями блоков фигуры
    def image(self):
        return self.figures[self.type][self.rotation]

"""Класс для игры, ее функции"""
class Tetris:
    x = 0
    y = 0
    # Инициализация переменных и игрового поля:
    def __init__(self, height, width):
        self.score = 0       # количество заполненных линий
        self.state = True    # статус игры
        self.block_Len = 30  # размер квадратиков
        self.figure = 0      # Текущая фигура
        self.height = height # размер поля по высоте
        self.width = width   # размер поля по ширине
        self.field = []      # игровое поле (двумерный массив заполенный изначально нулям)

        #создаём пустое поле
        for _ in range(height):
            new_line = []
            for _ in range(width):
                new_line.append(0) #заполняем его нулями
            self.field.append(new_line)

    #Создаём новую фигуру на поле
    def new_figure(self):
        self.figure = Figure(3, 0)

    #пересечения с другими блоками: возращает True, если нельзя двигаться в том направлении, куда захотели
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i*4 + j in self.figure.image(): #проверяем только саму фигуру, а не всё поле 4x4
                    #сравниваем выход за пределы по высоте и по ширине поля, и проверяем, не заполнена ли наше поле в данной позиции чем-то другим.
                    if (i+1 + self.figure.y > self.height) or \
                        (j+1 + self.figure.x > self.width) or \
                        (j + self.figure.x < 0) or            \
                        (self.field[i + self.figure.y][j + self.figure.x] != 0 ):
                        intersection = True
        return intersection

    #если появилась полностью заполненная линия блоками, то удаляем ее
    def break_lines(self):
        for i in range(1, self.height):
            empty = False # есть ли в линии пустые блоки?
            for j in range(self.width):
                if self.field[i][j] == 0:
                    empty = True # в линии есть пустые блоки, значит удалять ее не нужно.
                    break

            #если в линии нет пустых блоков, то
            if not empty:
                self.score += 1 #прибавляем к счётчику +1
                for i1 in range(i, 1, -1):
                    self.field[i1] = self.field[i1 - 1] # всё, что выше заполненной линии, сдвигаем вниз

    #опускаем фигурку вниз на 1 по у
    def go_down(self):
        self.figure.y += 1
        #проверяем, можно ли двигаться
        if self.intersects():
            self.figure.y -= 1 #если нельзя было, то возвращаем фигурку вверх на 1
            self.freeze() #останавливаем ее в этом положении

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image(): #для каждого блока фигуры.
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color # запоминаем ее блок на поле.

        self.break_lines() # проверяем на заполненность линий.
        
        self.new_figure()  # создаём новую фигуру:
        if self.intersects():  # если эта фигура при своём создании не может поставиться, то
            self.state = False # игра закончена.

    #двигаем фигуру вправо или влево
    def go_side(self, dx):
        old_x = self.figure.x #старое положение фигуры
        self.figure.x += dx #двигаем фигуру
        if self.intersects(): #если двигать нельзя было, то возвращаем старую позицию фигуры
            self.figure.x = old_x

    #поворот фигуры
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotation = (self.figure.rotation + 1) % 4
        if self.intersects():
            self.figure.rotation = old_rotation


"""Разметка поля"""
SIZE_THICKNESS = 1 #толщина разлиновки
MOVE_BLOCK = SIZE_THICKNESS #Насколько нужно сдвинуть блок, чтобы он не перекрывал разлиновку поля (выравниваем блок относительно линий)
CUT_BLOCK = SIZE_THICKNESS*2  #Насколько нужно обрезать блок фигуры, чтобы он не перекрывался разлиновкой поля
BLACK = (0, 0, 0)  #Цвет разлиновки поля и заднего фона для текста
WHITE = (255, 255, 255) #Фон игрового поля
RED = (255,0,0) #цвет надписей

"""Функционал"""
pygame.init()
size = (300, 600) #размер экрана
screen = pygame.display.set_mode(size) #создание экрана
pygame.display.set_caption("Tetris") #название приложения
clock = pygame.time.Clock()
Game_Is_Running = True #Статус игры
pressing_down = False #Нажата ли кнопка вниз
fps = 25

#Сообщения
def message(msg, color, sizeSym, MoveDown, MoveLeft):
    font_style = pygame.font.SysFont('Calibri', sizeSym, True, False)
    mesg = font_style.render(msg, True, color, BLACK)
    screen.blit(mesg, [size[0]/2 - MoveLeft, size[1]/2 + MoveDown ])

#Начальный экран
def StartScreen():
    pause = True
    while pause:
        message("Press any key to start", RED, 30, 0, 135)
        message("Press Enter to Pause", RED, 20, 40, 90)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pause = False
                return True
            if event.type == pygame.QUIT: #если нажали на крестик, то закрываем игру
                return False

def StartGame():
    return Tetris(size[1]//30, size[0]//30)


StartScreen()
game = StartGame()

go_left = False
go_right = False

while Game_Is_Running:
    #если фигуры нет, то создаём ее
    if not game.figure:
        game.new_figure()

    #опускаем фигуру вниз постоянно или ускоренно по нажатию кнопки "вниз"
    if pressing_down or clock.tick(fps):
        if game.state:
            game.go_down()

    if go_left:
        game.go_side(-1)
    if go_right:
        game.go_side(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #если нажали на крестик, то закрываем игру
            Game_Is_Running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: #если нажали "вверх", то поворачиваем фигуру
                game.rotate()
            if event.key == pygame.K_DOWN: #если нажали или зажали кнопку "вниз", от опускаем фигуру вниз
                pressing_down = True
            if event.key == pygame.K_LEFT:
                go_left = True
            if event.key == pygame.K_RIGHT:
                go_right = True
            if event.key == pygame.K_ESCAPE: #если нажали кнопку "ESC", то закрываем игру
                Game_Is_Running = False
            if event.key == pygame.K_SPACE: #если нажали пробел, то перезапускаем игру
                game = StartGame()
            if event.key == pygame.K_RETURN: #если нажали "Enter", то ставим игру на паузу
                Game_Is_Running = StartScreen()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                go_left = False
            if event.key == pygame.K_RIGHT:
                go_right = False

    screen.fill(WHITE)

    #разлиновка поля и отображение поставленных фигур на нём
    for i in range(game.height):
        for j in range(game.width):
            #рисуем квадрат поля (линии)
            pygame.draw.rect(screen, BLACK, [game.block_Len * j , game.block_Len * i , game.block_Len, game.block_Len], SIZE_THICKNESS)
            #если квадрат чем-то заполнен, то отображаем его содержимое
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]], 
                                 [game.block_Len * j + MOVE_BLOCK, game.block_Len * i + MOVE_BLOCK, 
                                  game.block_Len - CUT_BLOCK, game.block_Len - CUT_BLOCK])

    #Отображаем текущую фигуру на игровом поле
    if game.figure:
        for i in range(4):
            for j in range(4):
                if (i * 4 + j) in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.block_Len * (j + game.figure.x) + MOVE_BLOCK, #Положение квадратика на поле по X
                                      game.block_Len * (i + game.figure.y) + MOVE_BLOCK, #Положение квадратика на поле по Y
                                      game.block_Len - CUT_BLOCK, game.block_Len - CUT_BLOCK]) #размер квадратика

    #счёт
    font_style1 = pygame.font.SysFont('Calibri', 25, True, False)
    text = font_style1.render("Score: " + str(game.score), True, BLACK)
    screen.blit(text, [0, 0])
    
    #если Игра закончилась, выводим надписи
    if game.state == False:
        message("Game Over", RED, 60, 0, 140)
        message("Press Space to Restart", RED, 25, 60, 115)
        message("Press ESC to Exit", RED, 25, 85, 85)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
