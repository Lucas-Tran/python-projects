import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_cube():# Vertices of a cube
    vertices = [
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, -1],
        [-1, 1, -1],
        [1, 1, 1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, 1, 1]
    ]

    # Edges of the cube, each edge connects two vertices
    edges = (
        (0, 1, 2, 3),
        (4, 5, 6, 7)
    )

    glBegin(GL_QUADS)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def handle_movement(deltaTime):
    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[pygame.K_w]):
        glTranslatef(0, 0, -1 * deltaTime)
    elif (keys_pressed[pygame.K_s]):
        glTranslatef(0, 0, 1 * deltaTime)
    elif (keys_pressed[pygame.K_d]):
        glTranslatef(1 * deltaTime, 0, 0)
    elif (keys_pressed[pygame.K_a]):
        glTranslatef(-1 * deltaTime, 0, 0)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    #camera_pos = (0, 0, -2)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        deltaTime = 1/clock.tick(60)
        #handle_movement(deltaTime)

        glLoadIdentity()
        glTranslatef(0, 0, -2)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
