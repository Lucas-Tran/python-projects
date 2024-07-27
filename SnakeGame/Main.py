import numpy
import pygame
import GameObjects

# Initialize pygame
pygame.init()
    

# Define the screen caption and size
screenCaption = "Snake Game"
screenDimentions = numpy.array([1000, 500])
screen = pygame.display.set_mode(screenDimentions, pygame.RESIZABLE)
pygame.display.set_caption(screenCaption)

# Define the screen buffer
surface = pygame.Surface(screenDimentions)

# Define the clock
clock = pygame.time.Clock()

# Here is all the code for initializing
def Init():
    global joystickDirection
    GameObjects.Snake(screenDimentions / 2, [25, 25], 50)
    joystickDirection = numpy.array([1, 0])

# Here is all the code for Updating
def UpdateBuffer(deltaTime):
    global joystickDirection
    keysPressed = pygame.key.get_pressed()
    temp = numpy.array([keysPressed[pygame.K_RIGHT] - keysPressed[pygame.K_LEFT], keysPressed[pygame.K_DOWN] - keysPressed[pygame.K_UP]])
    allowedDirections = [numpy.array([1, 0]), numpy.array([-1, 0]), numpy.array([0, 1]), numpy.array([0, -1])]
    if any(numpy.array_equal(temp, move) for move in allowedDirections):
        joystickDirection = temp
    
    snakePosition += joystickDirection * snakeSpeed * deltaTime
    
    pygame.draw.rect(surface, (255, 0, 0), tuple(snakePosition - (snakeSize / 2)) + tuple(snakeSize))


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
            snakePosition += (numpy.array([event.w, event.h]) - screenDimentions) / 2
            screenDimentions = numpy.array([event.w, event.h])
            screen = pygame.display.set_mode(screenDimentions, pygame.RESIZABLE)
            surface = pygame.Surface(screenDimentions)
    
    # Clear and fill, and update the buffer
    surface.fill((0, 0, 255))
    UpdateBuffer(clock.tick(200) / 1000)

    # Stamp surface onto screen
    screen.blit(surface, (0, 0))
    # Update screen
    pygame.display.flip()

pygame.quit()
