from copy import deepcopy
import pygame
import numpy as np
import renderer
import vertex_transformer
import camera
import sys

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 500

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

vertices = [
    np.array([0, 0]),
    np.array([100, 100])
    ]

lines = [(0, 1, (255, 0, 0))]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    transformed_vertices = deepcopy(vertices)
    vertex_transformer.transform_vertices(transformed_vertices, camera)
    renderer.draw_lines(WINDOW, transformed_vertices, lines, pygame.draw.line)
    pygame.display.flip()
