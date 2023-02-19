import sys

import pygame
import configs
from canvas import Canvas
from predictor import Predictor
from _thread import start_new_thread


class Game:
    WIDTH, HEIGHT = configs.WIDTH, configs.HEIGHT
    FPS = configs.FPS

    def __init__(self):
        self.__pygame_init()
        self._game_preparation()
        self._run_game_cycle()

    def __pygame_init(self):
        pygame.init()
        pygame.display.set_caption("Digits prediction")

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 24)
        self.font_middle = pygame.font.SysFont('arial', 72)
        self.screen.fill(configs.WHITE)

    def _game_preparation(self):
        self._is_pressed = False
        self._canvas = Canvas()
        self.screen.blit(self.font.render('Нажмите X на клавиатуре, чтобы очистить холст', True, configs.BLACK),
                         (configs.CANVAS_X, configs.CANVAS_Y + 1.1 * configs.CANVAS_SIZE))
        self.predictor = Predictor()
        self.probs = [0] * 10
        self.predicted_digit = ""
        self.game_timer = 0
        self.is_taken = False
        start_new_thread(self._get_new_image, ())

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._is_pressed = True

            if event.type == pygame.MOUSEBUTTONUP:
                self._is_pressed = False

            if event.type == pygame.MOUSEMOTION and self._is_pressed:
                self._canvas.draw_on_canvas()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self._canvas.clear()
                if event.key == pygame.K_1:
                    picture = self._canvas.get_picture()
                    self.probs, self.predicted_digit = self.predictor.predict(picture)

    def _draw_prediction(self):
        digit_field = pygame.Surface((configs.CANVAS_SIZE // 2, configs.CANVAS_SIZE // 2))
        digit_field.fill(configs.WHITE)
        location = (configs.CANVAS_X + 1.1 * configs.CANVAS_SIZE, configs.CANVAS_Y + 1.1 * configs.CANVAS_SIZE)
        self.screen.blit(digit_field, location)
        self.screen.blit(self.font_middle.render(str(self.predicted_digit), True, configs.BLACK), location)

    def _get_new_image(self):
        while True:
            if self.game_timer == 1:
                picture = self._canvas.get_picture()
                self.probs, self.predicted_digit = self.predictor.predict(picture)

    def tick_timer(self):
        self.game_timer += 1
        self.game_timer %= configs.TIMER_PERIOD

    def _run_game_cycle(self):
        while True:
            self._process_events()

            self._canvas.draw(self.screen)
            self._draw_prediction()

            self.tick_timer()

            pygame.display.flip()
