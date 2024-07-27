import numpy
import pygame

# Initialize pygame
pygame.init()
    

# Define the screen caption and size
screenCaption = "Pygame"
screenDimentions = numpy.array([500, 200])
screen = pygame.display.set_mode(screenDimentions, pygame.RESIZABLE)
pygame.display.set_caption(screenCaption)

# Define the screen buffer
surface = pygame.Surface(screenDimentions)

# Here is all the code for initializing
def Init():
    return

# Here is all the code for Updating
def UpdateBuffer():
    return


# Initialize game
Init()

# Main Loop
running = True
while running:
    # Interate pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # We recieved the QUIT event so stop running
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # We recieved the VIDEORESIZE event so update the screen dimentions, screen, and surface
            screenDimentions = numpy.array([event.w, event.h])
            screen = pygame.display.set_mode(screenDimentions, pygame.RESIZABLE)
            surface = pygame.Surface(screenDimentions)

    # Clear and fill, and update the buffer
    surface.fill((0, 0, 255))
    UpdateBuffer()

    # Stamp surface onto screen
    screen.blit(surface, (0, 0))
    # Update screen
    pygame.display.flip()

pygame.quit()
