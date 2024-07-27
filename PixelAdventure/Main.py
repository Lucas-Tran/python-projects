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

    def __init__(self, x, y, width, height):
        self.rect = self.PLAYER_SPRITES["Idle_right"][1].get_rect(topleft = (x, y))
        self.direction = RIGHT_DIR
        self.velocity = Vector(0, 0)
        self.animation = 0
        self.state = "Idle"
        self.in_air = 0
        self.jump_count = 0

    def jump(self):
        if self.in_air < 3:
            self.jump_count = 1
            self.velocity.y = -self.JUMP_FORCE
            self.in_air = 3
        elif self.jump_count == 1 and abs(self.velocity.y) < (self.JUMP_FORCE / 5):
            self.jump_count = 2
            self.velocity.y = -self.JUMP_FORCE * 0.8

    def landed(self):
        self.jump_count = 0
        self.velocity.y = 0
        self.in_air = 0

    def hit_head(self):
        self.jump_count = 0
        self.velocity.y = 0

    def try_move(self, dx, dy, grid):
        self.rect.x += dx
        tile_rect = []
        if grid.grid_vs_rect(self.rect, tile_rect):
            if dx > 0:
                self.rect.right = tile_rect[0].left
            elif dx < 0:
                self.rect.left = tile_rect[0].right
        self.rect.y += dy
        tile_rect = []
        if grid.grid_vs_rect(self.rect, tile_rect):
            if dy > 0:
                self.rect.bottom = tile_rect[0].top
                self.landed()
            elif dy < 0:
                self.rect.top = tile_rect[0].bottom
                self.hit_head()

    def update(self, game_data):
        self.velocity.y += self.GRAVITY

        keys_pressed = pygame.key.get_pressed()

        def run_if_idle():
            if self.state == "Idle":
                self.animation = 0
                self.state = "Run"

        self.velocity.x /= self.FRICTION

        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0

        if keys_pressed[pygame.K_RIGHT]:
            self.velocity.x += self.ACCELERATION
            self.direction = RIGHT_DIR
            run_if_idle()
        elif keys_pressed[pygame.K_LEFT]:
            self.velocity.x -= self.ACCELERATION
            self.direction = LEFT_DIR
            run_if_idle()

        self.try_move(*self.velocity.to_tuple(), game_data[GRID])

        if self.velocity.y < 0:
            if self.jump_count == 2:
                self.state = "Double Jump"
            else:
                self.state = "Jump"
        elif self.velocity.y > 0:
            self.state = "Fall"
        elif self.velocity.x != 0:
            self.state = "Run"
        else:
            self.state = "Idle"

        self.in_air += 1
        self.animation += 0.5

        camera_position = game_data[CAMERA].position
        camera_position.x = self.rect.centerx - SCREEN_WIDTH / 2
        camera_position.y = self.rect.centery - SCREEN_HEIGHT / 2
        camera = game_data[CAMERA]
        if camera.position.y > 0:
            camera.position.y = 0

    def draw(self, window, camera):
        sprite_sheet = self.PLAYER_SPRITES[f"{self.state}_{self.direction}"]
        sprite_index = math.floor(self.animation) % len(sprite_sheet)
        sprite_image = sprite_sheet[sprite_index]
        draw_entity(window, sprite_image, (self.rect.x, self.rect.y), camera)

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

def update(game_data):
    game_data[PLAYER].update(game_data)

def draw(game_data):
    camera = game_data[CAMERA]
    WINDOW.blit(game_data[BACKGROUND], (-camera.position.x % 64 - 64, -camera.position.y % 64 - 64))
    game_data[PLAYER].draw(WINDOW, camera)
    game_data[GRID].draw_grid(WINDOW, game_data[TILES], camera)
    pygame.display.update()

def main():
    game_data = {
        CLOCK : pygame.time.Clock(),
        PLAYER : Player(500, 100, 30, 50),
        BACKGROUND : create_background(BACKGROUND_COLOR, 64),
        GRID : Tilemap(40, 30),
        TILES : split(join("Terrain", "Terrain (16x16).png"), 16, 16),
        CAMERA : Camera(0, 0)

    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game_data[PLAYER].jump()
        
        game_data[CLOCK].tick(FPS)

        update(game_data)
        draw(game_data)

    pygame.quit()

if __name__ == "__main__":
    main()