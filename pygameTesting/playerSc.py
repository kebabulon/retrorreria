import pygame
# import main

moving_right = False
moving_left = False
vertical_momentum = 5
air_timer = 0
gameMap = None
screen = None
blockColor = None
mapX = 0
mapY = 0
funny = 7
player_rect = pygame.Rect(400, 50, 5, 13)


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def playerdo():
    global player_rect, vertical_momentum, air_timer
    # pygame.draw.rect(screen, blockColor[0], (0, 0, mapX * funny, mapY * funny))
    tile_rects = []
    for x in range(round(player_rect.x / funny) - 2, round(player_rect.x / funny) + 2):
        for y in range(round(player_rect.y / funny) - 2, round(player_rect.y / funny) + 2):
            if gameMap[x][y].blockType != 0 and gameMap[x][y].liquid == False:
                tile_rects.append(pygame.Rect(x * funny, y * funny, funny, funny))
    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.3
    if vertical_momentum > 3:
        vertical_momentum = 3
    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1
    if collisions['top'] == True:
        air_timer = 0
        vertical_momentum = 0
    pygame.draw.rect(screen, blockColor[1], (player_rect.x, player_rect.y, 5, 13))
