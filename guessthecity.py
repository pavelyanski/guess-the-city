import pygame
import os
import sys
import requests
from random import choice, shuffle

START_SCREEN = "startscreen.jpg"
CHOICE_SCREEN = "choicicity.jpg"
LOSE_SCREEN = "losescreen.jpg"
WIN_SCREEN = "winscreen.jpg"
SIZE = WIDTH, HEIGHT = 600, 400
VIEW = ["sat", "map"]
CAPTION = "Угадай-ка город"
FPS = 60
CITIES = ["Сыктывкар", "Санкт-Петербург", "Нью-Йорк", "Рим"]
DICT_CITIES = {pygame.K_1: "Сыктывкар", pygame.K_2: "Санкт-Петербург", pygame.K_3: "Нью-Йорк", pygame.K_4: "Рим"}
COORDS = {"Сыктывкар": [(50.828505, 61.666294), (50.815956, 61.663849), (50.836853, 61.668838), (50.827227, 61.669529)],
          "Санкт-Петербург": [(30.219839, 59.973122), (30.316838, 59.950439), (30.315809, 59.938931),
                              (30.289575, 59.929720)],
          "Нью-Йорк": [(-74.045335, 40.688257), (-73.975606, 40.691028), (-73.951942, 40.720415),
                       (-73.997062, 40.728792)],
          "Рим": [(12.491978, 41.890318), (12.462872, 41.891131), (12.499312, 41.896696), (12.466826, 41.902304)]
          }
BLACK = pygame.Color("black")
RED = pygame.Color("red")
WHITE = pygame.Color("white")
BLUE = pygame.Color("blue")
YELLOW = pygame.Color("yellow")
GREEN = pygame.Color("green")
GOLD = pygame.Color("#ffd700")
city = None
COLOR_INACTIVE = pygame.Color('lightskyblue3')
WHITE = pygame.Color('WHITE')


def load_image(name, colorkey=None):
    fullname = os.path.join("img", name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def initialization():
    global clock, screen, FONT
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()
    FONT = pygame.font.Font(None, 22)


def start_screen():
    global clock
    fon = pygame.transform.scale(load_image(START_SCREEN), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()
                return
        pygame.display.flip()
        clock.tick(FPS)


def choose_city():
    global screen, clock, city
    fon = pygame.transform.scale(load_image(CHOICE_SCREEN), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 150
    for i in range(len(CITIES)):
        string_rendered = font.render(f"{str(i + 1)}) {CITIES[i]}", True, GOLD, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    text = "Загадайте город и нажмите соответствующую клавишу"
    font = pygame.font.SysFont(None, 26)
    text_coord = 30
    string_rendered = font.render(text, True, GOLD, BLACK)
    text_rect = string_rendered.get_rect()
    text_rect.top = text_coord - text_rect.height
    text_rect.x = WIDTH // 2 - text_rect.width // 2
    screen.blit(string_rendered, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    city = DICT_CITIES[event.key]
                    return
        pygame.display.flip()
        clock.tick(FPS)


def answer(screen):
    text = "Ответ:"
    font = pygame.font.SysFont(None, 24)
    string_rendered = font.render(text, True, WHITE)
    text_rect = string_rendered.get_rect()
    text_rect.x = 5
    text_rect.y = 5
    screen.blit(string_rendered, text_rect)


def check_answer(answer):
    if answer == city:
        win_screen()
    else:
        lose_screen()


def win_screen():
    global run
    run = False
    fon = pygame.transform.scale(load_image(WIN_SCREEN), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text = "Для продолжения нажмите пробел"
    font = pygame.font.SysFont(None, 25)
    text_coord = HEIGHT
    string_rendered = font.render(text, True, RED, BLACK)
    text_rect = string_rendered.get_rect()
    text_rect.top = text_coord - text_rect.height
    text_rect.x = WIDTH // 2 - text_rect.width // 2
    screen.blit(string_rendered, text_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def lose_screen():
    global run
    run = False
    fon = pygame.transform.scale(load_image(LOSE_SCREEN), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text = f"Правильный ответ: {city}"
    font = pygame.font.SysFont(None, 25)
    text_coord = 300
    string_rendered = font.render(text, True, RED, BLACK)
    text_rect = string_rendered.get_rect()
    text_rect.top = text_coord - text_rect.height
    text_rect.x = WIDTH // 2 - text_rect.width // 2
    screen.blit(string_rendered, text_rect)
    text = "Для продолжения нажмите пробел"
    font = pygame.font.SysFont(None, 25)
    text_coord = 320
    string_rendered = font.render(text, True, RED, BLACK)
    text_rect = string_rendered.get_rect()
    text_rect.top = text_coord - text_rect.height
    text_rect.x = WIDTH // 2 - text_rect.width // 2
    screen.blit(string_rendered, text_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.flip()
        clock.tick(FPS)


def main_game():
    global screen, clock, run
    run = True
    size = 0.001
    new_coords = COORDS[city][:]
    coords = []
    while len(new_coords) > 0:
        elem = choice(new_coords)
        new_coords.remove(elem)
        coords.append(elem)
    photo = 0
    view = choice(VIEW)
    x, y = coords[photo]
    picture = View(x, y, view, size)
    text = "Листай при помощи кнопки 'вправо'"
    font = pygame.font.SysFont(None, 25)
    text_coord = HEIGHT
    string_rendered = font.render(text, True, RED, BLACK)
    text_rect = string_rendered.get_rect()
    text_rect.top = text_coord - text_rect.height
    text_rect.x = WIDTH // 2 - text_rect.width // 2
    input_box = InputBox(60, 3, 200, 20, "")
    while run:
        clock.tick(60)
        screen.fill(BLACK)
        answer(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    photo = (photo + 1) % len(coords)
                    view = choice(VIEW)
                    x, y = coords[photo]
            input_box.handle_event(event)
        screen.blit(pygame.transform.scale(pygame.image.load(picture.get_picture()), (500, 370)), (50, 40))
        screen.blit(string_rendered, text_rect)
        picture = View(x, y, view, size)
        input_box.update()
        input_box.draw(screen)
        pygame.display.flip()


class View:
    def __init__(self, x, y, view, size):
        self.req = "http://static-maps.yandex.ru/1.x/?ll={},{}&spn={},{}&l={}"
        self.size = size
        self.map_request = self.req.format(x, y, size, size, view)
        self.map_file = "map.png"
        self.save_picture()

    def save_picture(self):
        response = requests.get(self.map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(self.map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        else:
            with open(self.map_file, "wb") as file:
                file.write(response.content)

    def get_picture(self):
        return self.map_file


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        global x, y, point, new_x, new_y
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = WHITE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    check_answer(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


pygame.quit()
if __name__ == "__main__":
    initialization()
    main_ran = True
    while main_ran:
        start_screen()
        choose_city()
        main_game()
