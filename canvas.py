import pygame
import configs


class Canvas:
    def __init__(self):
        self._canvas = pygame.Surface((configs.CANVAS_SIZE + 2 * configs.CANVAS_BORDER,
                                       configs.CANVAS_SIZE + 2 * configs.CANVAS_BORDER))
        self._subcanvas = pygame.Surface((configs.CANVAS_SIZE, configs.CANVAS_SIZE))
        self._subcanvas.fill(configs.WHITE)

    def _draw_circle(self, x, y):
        pygame.draw.circle(self._subcanvas, configs.BLACK, (x, y), configs.BRUSH_SIZE)

    @staticmethod
    def _check_canvas_borders(x, y):
        return configs.CANVAS_X + configs.CANVAS_BORDER <= x <= configs.CANVAS_X \
            + configs.CANVAS_BORDER + configs.CANVAS_SIZE and \
            configs.CANVAS_Y + configs.CANVAS_BORDER <= y \
            <= configs.CANVAS_Y + configs.CANVAS_BORDER + configs.CANVAS_SIZE

    def draw_on_canvas(self):
        x, y = pygame.mouse.get_pos()
        if self._check_canvas_borders(x, y):
            self._draw_circle(x - configs.CANVAS_X - configs.CANVAS_BORDER,
                              y - configs.CANVAS_Y - configs.CANVAS_BORDER)

    def draw(self, screen):
        screen.blit(self._canvas, (configs.CANVAS_X, configs.CANVAS_Y))
        screen.blit(self._subcanvas, (configs.CANVAS_X + configs.CANVAS_BORDER,
                                      configs.CANVAS_Y + configs.CANVAS_BORDER))

    def clear(self):
        self._subcanvas.fill(configs.WHITE)

    def get_picture(self):
        pixel_array = pygame.surfarray.array2d(pygame.transform.scale(self._subcanvas,
                                                                      (configs.OUTPUT_SIZE, configs.OUTPUT_SIZE)))
        pixel_array = (pixel_array.astype("float32") / configs.MAX_BRIGHTNESS).T
        pixel_array = 1 - pixel_array.reshape(configs.INPUT_SHAPE)
        return pixel_array
