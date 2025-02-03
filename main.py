import argparse
import pygame
import transformer
from path_to_function import *
from constants import Constants
from time import time

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--path-file', type=str, help='Path to the function file')
args = parser.parse_args()

path_file = Constants.PATH_FILE

if args.path_file:
    path_file = args.path_file


def drawComplexPoint(num: complex, surf: pygame.surface.Surface) -> None:
    coord = (
        int(num.real * Constants.GRAPH_SCALE + Constants.ORIGIN_POSITION[0]),
        int(-num.imag * Constants.GRAPH_SCALE + Constants.ORIGIN_POSITION[1]),
    )
    pygame.draw.circle(surf, (255, 255, 255), coord, 1)


def drawComplexLine(num1: complex, num2: complex,
                    surf: pygame.surface.Surface) -> None:
    coord1 = (
        int(num1.real * Constants.GRAPH_SCALE + Constants.ORIGIN_POSITION[0]),
        int(-num1.imag * Constants.GRAPH_SCALE + Constants.ORIGIN_POSITION[1]),
    )
    coord2 = (
        int(num2.real * Constants.GRAPH_SCALE + Constants.ORIGIN_POSITION[0]),
        int(-num2.imag * Constants.GRAPH_SCALE + Constants.ORIGIN_POSITION[1]),
    )
    pygame.draw.aaline(surf, Constants.TRACK_COLOR, coord1, coord2)


def drawComplexCircle(circles, surf) -> None:
    for circle in circles:
        x = circle[
            "pos"].real * Constants.GRAPH_SCALE + Constants.ORIGIN_POSITION[0]
        y = -circle[
            "pos"].imag * Constants.GRAPH_SCALE + Constants.ORIGIN_POSITION[1]
        radius = circle["radius"] * Constants.GRAPH_SCALE
        pygame.draw.circle(surf, Constants.CIRCLES_COLOR, (int(x), int(y)),
                           max(int(radius), 1), 1)


def targetFunction(t: float) -> complex:
    return functionFromPath(readPathFromFile((path_file)), t)


def main():
    print("computing parameters ...")
    time_start = time()
    parameters = transformer.transform(targetFunction, Constants.ORDER,
                                       Constants.INTEGRATE_PRECISION)
    time_cost = time() - time_start
    print("parameters got, time cost: {:.2f}s".format(time_cost))
    print("starting gui ...")

    pygame.init()
    screen = pygame.display.set_mode(
        (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))
    pygame.display.set_caption("Fourier Graph")
    clock = pygame.time.Clock()
    t = 0.0
    track = pygame.surface.Surface(
        (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))
    track.fill(Constants.BACKGROUND_COLOR)
    track.set_colorkey(Constants.BACKGROUND_COLOR)
    lastpoint = None

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
        pygame.draw.circle(screen, Constants.ORIGIN_COLOR,
                           Constants.ORIGIN_POSITION, 1)
        # draw x y axis
        pygame.draw.line(
            screen,
            Constants.X_AXIS_COLOR,
            (0, Constants.ORIGIN_POSITION[1]),
            (Constants.WINDOW_WIDTH, Constants.ORIGIN_POSITION[1]),
        )
        pygame.draw.line(
            screen,
            Constants.Y_AXIS_COLOR,
            (Constants.ORIGIN_POSITION[0], 0),
            (Constants.ORIGIN_POSITION[0], Constants.WINDOW_HEIGHT),
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
