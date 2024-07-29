import pygame
import sys

from pygame.locals import *

DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3
ANIMATION = [0, 1, 0, 2]
BLINK = ["#fff", "#ffc", "#ff8", "#fe4", "#ff8", "#ffc"]
DOT = 20

img_bg = []
img_pen = []
img_red = []
img_kuma = []
img_title = None
img_ending = None

map_data = []  # 미로용 리스트

idx = 0
tmr = 0
stage = 1
score = 0
life = 3
candy = 0

pen_x = 0
pen_y = 0
pen_d = 0
pen_a = 0


def init_resources():
    global img_bg, img_pen, img_red, img_kuma, img_title, img_ending

    img_bg = [
        pygame.image.load("images/chip00.png").convert(),
        pygame.image.load("images/chip01.png").convert(),
        pygame.image.load("images/chip02.png").convert(),
        pygame.image.load("images/chip03.png").convert()
    ]

    img_pen = [
        pygame.image.load("images/pen00.png").convert_alpha(),
        pygame.image.load("images/pen01.png").convert_alpha(),
        pygame.image.load("images/pen02.png").convert_alpha(),
        pygame.image.load("images/pen03.png").convert_alpha(),
        pygame.image.load("images/pen04.png").convert_alpha(),
        pygame.image.load("images/pen05.png").convert_alpha(),
        pygame.image.load("images/pen06.png").convert_alpha(),
        pygame.image.load("images/pen07.png").convert_alpha(),
        pygame.image.load("images/pen08.png").convert_alpha(),
        pygame.image.load("images/pen09.png").convert_alpha(),
        pygame.image.load("images/pen10.png").convert_alpha(),
        pygame.image.load("images/pen11.png").convert_alpha(),
        pygame.image.load("images/pen_face.png").convert_alpha(),
    ]

    img_red = [
        pygame.image.load("images/red00.png").convert_alpha(),
        pygame.image.load("images/red01.png").convert_alpha(),
        pygame.image.load("images/red02.png").convert_alpha(),
        pygame.image.load("images/red03.png").convert_alpha(),
        pygame.image.load("images/red04.png").convert_alpha(),
        pygame.image.load("images/red05.png").convert_alpha(),
        pygame.image.load("images/red06.png").convert_alpha(),
        pygame.image.load("images/red07.png").convert_alpha(),
        pygame.image.load("images/red08.png").convert_alpha(),
        pygame.image.load("images/red09.png").convert_alpha(),
        pygame.image.load("images/red10.png").convert_alpha(),
        pygame.image.load("images/red11.png").convert_alpha(),
    ]

    img_kuma = [
        pygame.image.load("images/kuma00.png").convert_alpha(),
        pygame.image.load("images/kuma01.png").convert_alpha(),
        pygame.image.load("images/kuma02.png").convert_alpha(),
    ]

    img_title = pygame.image.load("images/title.png").convert_alpha()
    img_ending = pygame.image.load("images/ending.png").convert_alpha()


def set_stage():  # 스테이지 데이터 설정
    global map_data

    map_data = [
        [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
        [0, 2, 3, 3, 2, 1, 1, 2, 3, 3, 2, 0],
        [0, 3, 0, 0, 3, 3, 3, 3, 0, 0, 3, 0],
        [0, 3, 1, 1, 3, 0, 0, 3, 1, 1, 3, 0],
        [0, 3, 2, 2, 3, 0, 0, 3, 2, 2, 3, 0],
        [0, 3, 0, 0, 3, 1, 1, 3, 0, 0, 3, 0],
        [0, 3, 1, 1, 3, 3, 3, 3, 1, 1, 3, 0],
        [0, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]


def set_character_pos():  # 캐릭터 시작 위치
    global pen_x, pen_y, pen_d, pen_a

    pen_x = 90
    pen_y = 90
    pen_d = DIR_DOWN
    pen_a = 3


def draw_screen(screen):
    for y in range(9):
        for x in range(12):
            screen.blit(img_bg[map_data[y][x]], [x * 60, y * 60])

    screen.blit(img_pen[pen_a], [pen_x - 30, pen_y - 30])


def check_wall(cx, cy, di, dot):  # 각 방향에 벽 존재 여부 확인
    chk = False
    if di == DIR_UP:
        mx = int((cx - 30) / 60)
        my = int((cy - 30 - dot) / 60)
        if map_data[my][mx] <= 1:  # 좌상
            chk = True
        mx = int((cx + 29) / 60)
        if map_data[my][mx] <= 1:  # 우상
            chk = True
    if di == DIR_DOWN:
        mx = int((cx - 30) / 60)
        my = int((cy + 29 + dot) / 60)
        if map_data[my][mx] <= 1:  # 좌하
            chk = True
        mx = int((cx + 29) / 60)
        if map_data[my][mx] <= 1:  # 우하
            chk = True
    if di == DIR_LEFT:
        mx = int((cx - 30 - dot) / 60)
        my = int((cy - 30) / 60)
        if map_data[my][mx] <= 1:  # 좌상
            chk = True
        mx = int((cy + 29) / 60)
        if map_data[my][mx] <= 1:  # 좌하
            chk = True
    if di == DIR_RIGHT:
        mx = int((cx + 29 + dot) / 60)
        my = int((cy - 30) / 60)
        if map_data[my][mx] <= 1:  # 우상
            chk = True
        mx = int((cy + 29) / 60)
        if map_data[my][mx] <= 1:  # 우하
            chk = True
    return chk


def move_penpen(key):  # 펜펜 움직이기
    global score, candy, pen_x, pen_y, pen_d, pen_a

    if key[K_UP] == 1:
        pen_d = DIR_UP
        if check_wall(pen_x, pen_y, pen_d, DOT) == False:
            pen_y = pen_y - DOT
    elif key[K_DOWN] == 1:
        pen_d = DIR_DOWN
        if check_wall(pen_x, pen_y, pen_d, DOT) == False:
            pen_y = pen_y + DOT
    elif key[K_LEFT] == 1:
        pen_d = DIR_LEFT
        if check_wall(pen_x, pen_y, pen_d, DOT) == False:
            pen_x = pen_x - DOT
    elif key[K_RIGHT] == 1:
        pen_d = DIR_RIGHT
        if check_wall(pen_x, pen_y, pen_d, DOT) == False:
            pen_x = pen_x + DOT
    pen_a = pen_d * 3 + ANIMATION[tmr % 4]
    mx = int(pen_x / 60)
    my = int(pen_y / 60)
    if map_data[my][mx] == 3:  # 사탕에 닿았는가?
        score = score + 100
        map_data[my][mx] = 2
        candy = candy - 1


def main():
    global key, tmr, score
    pygame.init()
    pygame.display.set_caption("PenPen")
    screen = pygame.display.set_mode((720, 540))
    init_resources()
    set_stage()
    set_character_pos()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
        tmr += 1
        draw_screen(screen)

        move_penpen(key)

        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
