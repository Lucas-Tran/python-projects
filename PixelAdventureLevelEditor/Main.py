import pygame
import random
import math
import Maps
from os import listdir
from os.path import isfile, join
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Pixel Adventure")

FPS = 60

RIGHT_DIR = "right"
LEFT_DIR = "left"

CLOCK = "clock"
PLAYER = "player"
BACKGROUND = "background"
GRID = "grid"
TILES = "tiles"
CAMERA = "camera"
LEVEL_EDITOR = "level_editor"

PLAYER_TYPE = "Mask Dude"
BACKGROUND_COLOR = "Blue"

def flip_sprites(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def split(path_to_sprite_sheet, width, height):
    sprite_sheet = pygame.image.load(join("Assets", path_to_sprite_sheet)).convert_alpha()

    sprites = []
    rows = sprite_sheet.get_height() // height
    columns = sprite_sheet.get_width() // width

    for row in range(rows):
        sprites.append([])
        for column in range(columns):
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            reigion = pygame.Rect(column * width, row * height, width, height)
            sprite.blit(sprite_sheet, (0, 0), reigion)
            sprites[row].append(pygame.transform.scale2x(sprite))

    return sprites

def split_all_under(path_to_directory, width, height, contain_flipped = False):
    sprite_sheets = [file_name for file_name in listdir(join("Assets", path_to_directory)) if isfile(join("Assets", path_to_directory, file_name))]

    sprites = {}

    for sprite_sheet in sprite_sheets:
        split_row = split(join(path_to_directory, sprite_sheet), width, height)[0]

        if contain_flipped:
            sprites[sprite_sheet.replace(".png", f"_{RIGHT_DIR}")] = split_row
            sprites[sprite_sheet.replace(".png", f"_{LEFT_DIR}")] = flip_sprites(split_row)
        else:
            sprites[sprite_sheet.replace(".png", "")] = split_row

    return sprites

def create_background(background_color, tile_size):
    tile = pygame.image.load(join("Assets", "Background", background_color) + ".png")
    background_image = pygame.Surface((SCREEN_WIDTH + tile_size, SCREEN_HEIGHT + tile_size))
    rows = SCREEN_HEIGHT // tile_size + 2
    columns = SCREEN_WIDTH // tile_size + 2
    for row in range(rows):
        for column in range(columns):
            background_image.blit(tile, (column * tile_size, row * tile_size))
    return background_image

def draw_entity(window, sprite_image, position, camera):
    window.blit(sprite_image, (position[0] - camera.position.x, position[1] - camera.position.y))

class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self):
        return (self.x, self.y)

class Player():
    GRAVITY = 0.5
    JUMP_FORCE = 15
    ACCELERATION = 3.5
    FRICTION = 3
    PLAYER_SPRITES = split_all_under(join("Main Characters", PLAYER_TYPE), 32, 32, True)

    def __init__(self, x, y):
        self.position = Vector(x, y)

    def update(self, game_data):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_RIGHT]:
            self.position.x += 5
        elif keys_pressed[pygame.K_LEFT]:
            self.position.x -= 5
        if keys_pressed[pygame.K_UP]:
            self.position.y -= 5
        elif keys_pressed[pygame.K_DOWN]:
            self.position.y += 5

        camera = game_data[CAMERA]
        camera.position = self.position
        if camera.position.y > 0:
            camera.position.y = 0

class Camera():
    def __init__(self, x, y):
        self.position = Vector(x, y)

class Tilemap():
    def __init__(self, width, height):
        self.array = Maps.default_map(width, height, 0, 6)

    def get_grid_tile(self, x, y):
        if 0 <= x < len(self.array) and 0 <= y < len(self.array[x]):
            return self.array[x][y]
        return None
    
    def set_grid_tile(self, x, y, tile):
        if 0 <= x < len(self.array) and 0 <= y < len(self.array[x]):
            self.array[x][y] = tile
    
    def draw_grid(self, window, tiles, camera):
        print(camera.position.x)
        for x in range(len(self.array)):
            for y in range(len(self.array[0])):
                tile = self.get_grid_tile(x, y)
                if tile != None:
                    draw_entity(window, tiles[tile[0]][tile[1]], (x * 32, SCREEN_HEIGHT - (32 + y * 32)), camera)

    def grid_vs_rect(self, rect, out_tile_rect):
        for x in range(len(self.array)):
            for y in range(len(self.array[x])):
                if self.get_grid_tile(x, y) != None:
                    tile_rect = pygame.Rect(x * 32, SCREEN_HEIGHT - (y + 1) * 32, 32, 32)
                    if tile_rect.colliderect(rect):
                        out_tile_rect.append(tile_rect)
                        return True
        return False

class Level_Editor():
    def __init__(self, tile, editor_on):
        self.tile = tile
        self.pallete_on = False
        self.editor_on = editor_on
        self.white_square = pygame.image.load("white.png").convert_alpha()
        self.white_square.set_alpha(100)

    def get_grid_pos_from_screen(self, game_data, screen_pos):
        mouse_x, mouse_y = screen_pos
        
        mouse_x += game_data[CAMERA].position.x
        mouse_y += game_data[CAMERA].position.y

        mouse_grid_x = math.floor(mouse_x / 32)
        mouse_grid_y = math.floor((SCREEN_HEIGHT - mouse_y) / 32)

        return mouse_grid_x, mouse_grid_y

    def update(self, game_data):
        if not self.editor_on:
            self.pallete_on = False

    def draw(self, window, game_data):
        if self.editor_on:
            if self.tile != None:
                mouse_grid = self.get_grid_pos_from_screen(game_data, pygame.mouse.get_pos())
                tile = game_data[TILES][self.tile[0]][self.tile[1]].convert_alpha()
                tile.set_alpha(150)
                draw_entity(window,
                            tile, 
                            (mouse_grid[0] * 32, SCREEN_HEIGHT - ((mouse_grid[1] + 1) * 32)), 
                            game_data[CAMERA]
                            )
            
            if self.pallete_on:
                pygame.draw.rect(window, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
                tiles = game_data[TILES]
                for row in range(len(tiles)):
                    for column in range(len(tiles[row])):
                        window.blit(tiles[row][column], (column * 32, row * 32))
                        tile_rect = pygame.Rect(column * 32, row * 32, 32, 32)
                        if tile_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                            self.tile = (row, column)
                        if self.tile == (row, column):
                            window.blit(self.white_square, (column * 32, row * 32))

    def place_tile_at_screen_pos(self, game_data, screen_pos, tile):
        grid_pos = self.get_grid_pos_from_screen(game_data, screen_pos)
        game_data[GRID].set_grid_tile(*grid_pos, tile)

def update(game_data):
    if not game_data[LEVEL_EDITOR].pallete_on:
        game_data[PLAYER].update(game_data)
    game_data[LEVEL_EDITOR].update(game_data)

def draw(game_data):
    camera = game_data[CAMERA]
    WINDOW.blit(game_data[BACKGROUND], (-camera.position.x % 64 - 64, -camera.position.y % 64 - 64))
    game_data[GRID].draw_grid(WINDOW, game_data[TILES], camera)
    game_data[LEVEL_EDITOR].draw(WINDOW, game_data)
    pygame.display.update()

def main():
    game_data = {
        CLOCK : pygame.time.Clock(),
        PLAYER : Player(500, 100),
        BACKGROUND : create_background(BACKGROUND_COLOR, 64),
        GRID : Tilemap(40, 30),
        TILES : split(join("Terrain", "Terrain (16x16).png"), 16, 16),
        CAMERA : Camera(0, 0),
        LEVEL_EDITOR : Level_Editor((0, 7), True)

    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and game_data[LEVEL_EDITOR].editor_on:
                    level_editor = game_data[LEVEL_EDITOR]
                    if level_editor.pallete_on:
                        level_editor.pallete_on = False
                    else:
                        level_editor.pallete_on = True
                elif event.key == pygame.K_e and game_data[LEVEL_EDITOR].editor_on:
                    mouse_grid = game_data[LEVEL_EDITOR].get_grid_pos_from_screen(game_data, pygame.mouse.get_pos())
                    game_data[LEVEL_EDITOR].tile = game_data[GRID].get_grid_tile(*mouse_grid)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_data[LEVEL_EDITOR].pallete_on and game_data[LEVEL_EDITOR].editor_on:
                    game_data[LEVEL_EDITOR].place_tile_at_screen_pos(game_data, event.pos, game_data[LEVEL_EDITOR].tile)
        
        game_data[CLOCK].tick(FPS)

        update(game_data)
        draw(game_data)

    pygame.quit()

if __name__ == "__main__":
    main()