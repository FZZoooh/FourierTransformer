import pygame
import transformer
import my_functions
from constants import Constants


# pre-calculate
originPosition = (Constants.WINDOW_WIDTH / 2, Constants.WINDOW_HEIGHT / 2)
# adjust precision
transformer.setPrecision(600.0)


targetFunction = my_functions.myFunctions[Constants.TARGET_FUNCITON]


def drawComplexPoint(num: complex, surf: pygame.surface.Surface) -> None:
    coord = (
        int(num.real * Constants.GRAPH_SCALE + originPosition[0]),
        int(-num.imag * Constants.GRAPH_SCALE + originPosition[1]),
    )
    pygame.draw.circle(surf, (255, 255, 255), coord, 1)


def drawComplexLine(num1: complex, num2: complex, surf: pygame.surface.Surface) -> None:
    coord1 = (
        int(num1.real * Constants.GRAPH_SCALE + originPosition[0]),
        int(num1.imag * Constants.GRAPH_SCALE + originPosition[1]),
    )
    coord2 = (
        int(num2.real * Constants.GRAPH_SCALE + originPosition[0]),
        int(num2.imag * Constants.GRAPH_SCALE + originPosition[1]),
    )
    pygame.draw.aaline(surf, Constants.TRACK_COLOR, coord1, coord2)


def drawComplexCircle(circles, surf) -> None:
    for circle in circles:
        x = circle["pos"].real * Constants.GRAPH_SCALE + originPosition[0]
        y = circle["pos"].imag * Constants.GRAPH_SCALE + originPosition[1]
        radius = circle["radius"] * Constants.GRAPH_SCALE
        pygame.draw.circle(
            surf, Constants.CIRCLES_COLOR, (int(x), int(y)), max(int(radius), 1), 1
        )


def main():
    pygame.init()
    screen = pygame.display.set_mode((Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))
    pygame.display.set_caption("Fourier Graph")
    clock = pygame.time.Clock()
    t = 0.0
    track = pygame.surface.Surface((Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))
    track.fill(Constants.BACKGROUND_COLOR)
    track.set_colorkey(Constants.BACKGROUND_COLOR)
    lastpoint = None

    parameters = transformer.transform(targetFunction, Constants.ORDER)
    print("parameters got")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(Constants.BACKGROUND_COLOR)
        t += Constants.DELTA_T
        if t >= 1.0:
            t = 0.0
        # draw origin
        pygame.draw.circle(screen, Constants.ORIGIN_COLOR, originPosition, 1)
        # draw x y axis in blue and green
        pygame.draw.line(
            screen,
            Constants.X_AXIS_COLOR,
            (0, originPosition[1]),
            (Constants.WINDOW_WIDTH, originPosition[1]),
        )
        pygame.draw.line(
            screen,
            Constants.Y_AXIS_COLOR,
            (originPosition[0], 0),
            (originPosition[0], Constants.WINDOW_HEIGHT),
        )
        circles = transformer.getCircles(parameters, t)
        point = circles[-1]["pos"]
        drawComplexCircle(circles, screen)
        if lastpoint:
            drawComplexLine(lastpoint, point, track)
        lastpoint = point
        screen.blit(track, (0, 0))
        pygame.display.flip()
        clock.tick(Constants.FPS)


main()
