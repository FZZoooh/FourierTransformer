import argparse
import pygame
import transformer
import os
from path_to_function import *
from config import Config
from time import time
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--path-file', type=str)
parser.add_argument('--graph-scale', type=float)
parser.add_argument('--adaptive-scale', action='store_true')
parser.add_argument('--speed', type=float)
parser.add_argument('--repeat', action='store_true')
args = parser.parse_args()

if args.path_file:
    Config.PATH = args.path_file
if args.graph_scale:
    Config.GRAPH_SCALE = args.graph_scale
if args.speed:
    Config.DELTA_T *= args.speed


def drawComplexPoint(num: complex, surf: pygame.surface.Surface) -> None:
    coord = (
        int(num.real * Config.GRAPH_SCALE + Config.ORIGIN_POSITION[0]),
        int(num.imag * Config.GRAPH_SCALE + Config.ORIGIN_POSITION[1]),
    )
    pygame.draw.circle(surf, (255, 255, 255), coord, 1)


def drawComplexLine(num1: complex, num2: complex,
                    surf: pygame.surface.Surface) -> None:
    coord1 = (
        int(num1.real * Config.GRAPH_SCALE + Config.ORIGIN_POSITION[0]),
        int(num1.imag * Config.GRAPH_SCALE + Config.ORIGIN_POSITION[1]),
    )
    coord2 = (
        int(num2.real * Config.GRAPH_SCALE + Config.ORIGIN_POSITION[0]),
        int(num2.imag * Config.GRAPH_SCALE + Config.ORIGIN_POSITION[1]),
    )
    pygame.draw.aaline(surf, Config.TRACK_COLOR, coord1, coord2)


def drawComplexCircle(circles, surf) -> None:
    for circle in circles:
        x = circle["pos"].real * Config.GRAPH_SCALE + Config.ORIGIN_POSITION[0]
        y = circle["pos"].imag * Config.GRAPH_SCALE + Config.ORIGIN_POSITION[1]
        radius = circle["radius"] * Config.GRAPH_SCALE
        pygame.draw.circle(surf, Config.CIRCLES_COLOR, (int(x), int(y)),
                           max(int(radius), 1), 1)


def count_files(directory):
    num_files = 0
    for root, dirs, files in os.walk(directory):
        num_files += len(files)
    return num_files


def main():
    multiple_paths = os.path.isdir(Config.PATH)
    print("computing parameters ...")
    time_start = time()
    if multiple_paths:
        parameters_list = []
        speedconfig = open(Config.PATH + "/speed.config").read().splitlines()
        sizeconfig = open(Config.PATH + "/size.config").read().split()
        if args.adaptive_scale:
            Config.GRAPH_SCALE = min(
                Config.WINDOW_WIDTH / float(sizeconfig[0]),
                Config.WINDOW_HEIGHT / float(sizeconfig[1]))
        num_of_paths = count_files(
            Config.PATH) - 2  # exclude speed.config and size.config
        for i in range(num_of_paths):
            speedconfig[i] = float(speedconfig[i])
        for path_index in tqdm(range(num_of_paths)):
            file_path = Config.PATH + "/" + os.path.basename(
                Config.PATH) + str(path_index)
            target_path = readPathFromFile(file_path)
            parameters_list.append(
                transformer.transform(target_path, Config.ORDER,
                                      Config.INTEGRATE_PRECISION))

    else:
        target_path = readPathFromFile(Config.PATH)
        parameters_list = [
            transformer.transform(target_path, Config.ORDER,
                                  Config.INTEGRATE_PRECISION)
        ]
    time_cost = time() - time_start
    print("parameters got, time cost: {:.2f}s".format(time_cost))
    print("starting gui ...")

    pygame.init()
    screen = pygame.display.set_mode(
        (Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
    pygame.display.set_caption("Fourier Graph")
    clock = pygame.time.Clock()
    t = 0.0
    track = pygame.surface.Surface((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
    track.fill(Config.BACKGROUND_COLOR)
    track.set_colorkey(Config.BACKGROUND_COLOR)
    lastpoint = None

    graph_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(Config.BACKGROUND_COLOR)
        if multiple_paths:
            t += Config.DELTA_T * speedconfig[graph_index]
        else:
            t += Config.DELTA_T
        if t >= 1.0:
            graph_index += 1
            lastpoint = None
            if graph_index >= len(parameters_list):
                if args.repeat:
                    graph_index = 0
                else:
                    screen.fill(Config.BACKGROUND_COLOR)
                    screen.blit(track, (0, 0))
                    pygame.display.flip()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                        clock.tick(Config.FPS)
            t = 0.0
        # draw origin
        pygame.draw.circle(screen, Config.ORIGIN_COLOR, Config.ORIGIN_POSITION,
                           1)
        # draw x y axis
        pygame.draw.line(
            screen,
            Config.X_AXIS_COLOR,
            (0, Config.ORIGIN_POSITION[1]),
            (Config.WINDOW_WIDTH, Config.ORIGIN_POSITION[1]),
        )
        pygame.draw.line(
            screen,
            Config.Y_AXIS_COLOR,
            (Config.ORIGIN_POSITION[0], 0),
            (Config.ORIGIN_POSITION[0], Config.WINDOW_HEIGHT),
        )

        circles = transformer.getCircles(parameters_list[graph_index], t)
        point = circles[-1]["pos"]
        drawComplexCircle(circles, screen)
        if lastpoint:
            drawComplexLine(lastpoint, point, track)
        lastpoint = point
        screen.blit(track, (0, 0))
        pygame.display.flip()
        clock.tick(Config.FPS)


main()
