import playerSc
import random
import json
from json import JSONEncoder
import pygame
import perlin

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("retroreria ALPHA 0.11")
icon = pygame.image.load("sprites/logo_test.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

blockColor = [(0, 0, 0), (255, 255, 153), (100, 149, 237), (139, 69, 19), (138, 133, 133), (31, 152, 45)]
mapX = 80
mapY = 50
funny = 9
blockRn = 0
time_elapsed_since_last_action = 0

moving_right = False
moving_left = False
vertical_momentum = 5
air_timer = 0
player_rect = pygame.Rect(400, 50, 5, 13)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


class strucTile:
    def __init__(self, blockType):
        self.blockType = blockType
        self.move = False
        self.liquid = False
        self.hard = False


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def map_create():
    newMap = [[strucTile(0) for y in range(0, mapY)] for x in range(0, mapX)]
    noise = perlin.Perlin(6)
    time = [i for i in range(80)]
    values = [noise.valueAt(i) for i in time]
    values = [values[i] * 12 for i in time]
    values = [abs(round(values[i])) for i in time]
    for y in range(0, mapY):
        for x in range(0, mapX):
            if y < 12:
                newMap[x][values[x] + 13 + y].blockType = 3
            if newMap[x][y].blockType == 3 and newMap[x][y - 1].blockType == 0:
                newMap[x][y].blockType = 5
            if newMap[x][y].blockType == 3 and newMap[x][y + 1].blockType == 0:
                newMap[x][y].blockType = 4
            if newMap[x][y].blockType == 4 and y < mapY - 1:
                newMap[x][y + 1].blockType = 4
    return newMap


def draw_map(mapToDraw):
    for x in range(0, mapX):
        for y in range(0, mapY):
            if mapToDraw[x][y].blockType == 1:
                pygame.draw.rect(screen, blockColor[1], (x * funny, y * funny, funny, funny))
            elif mapToDraw[x][y].blockType == 2:
                pygame.draw.rect(screen, blockColor[2], (x * funny, y * funny, funny, funny))
            elif mapToDraw[x][y].blockType == 3:
                pygame.draw.rect(screen, blockColor[3], (x * funny, y * funny, funny, funny))
            elif mapToDraw[x][y].blockType == 4:
                pygame.draw.rect(screen, blockColor[4], (x * funny, y * funny, funny, funny))
            elif mapToDraw[x][y].blockType == 5:
                pygame.draw.rect(screen, blockColor[5], (x * funny, y * funny, funny, funny))


def check(mapToCheck):
    for y in range(mapY - 1, -1, -1):
        for x in range(0, mapX):
            if mapToCheck[x][y].blockType != 0:
                mapToCheck[x][y].move = True
            if mapToCheck[x][y].blockType == 1:
                mapToCheck[x][y].liquid = False
                mapToCheck[x][y].hard = False
            elif mapToCheck[x][y].blockType == 2:
                mapToCheck[x][y].liquid = True
                mapToCheck[x][y].hard = False
            elif mapToCheck[x][y].blockType == 3 or mapToCheck[x][y].blockType == 4 or mapToCheck[x][y].blockType == 5:
                mapToCheck[x][y].liquid = False
                mapToCheck[x][y].hard = True


def simulate(mapToSimulate):
    for y in range(mapY - 1, -1, -1):
        for x in range(0, mapX):
            try:
                if mapToSimulate[x][y].move == True:
                    # sand
                    if mapToSimulate[x][y].blockType == 1:
                        if mapToSimulate[x][y + 1].blockType == 0:
                            mapToSimulate[x][y].blockType = 0
                            mapToSimulate[x][y].move = False
                            mapToSimulate[x][y + 1].blockType = 1
                        elif mapToSimulate[x][y + 1].liquid == True:
                            oldB = mapToSimulate[x][y].blockType
                            mapToSimulate[x][y].blockType = mapToSimulate[x][y + 1].blockType
                            mapToSimulate[x][y].move = False
                            mapToSimulate[x][y + 1].blockType = oldB
                        elif mapToSimulate[x][y + 1] != 0 and mapToSimulate[x - 1][y + 1].blockType == 0 and \
                                mapToSimulate[x][y + 1].hard == False:
                            mapToSimulate[x][y].blockType = 0
                            mapToSimulate[x][y].move = False
                            mapToSimulate[x - 1][y + 1].blockType = 1
                        elif mapToSimulate[x][y + 1] != 0 and mapToSimulate[x + 1][y + 1].blockType == 0 and \
                                mapToSimulate[x][y + 1].hard == False:
                            mapToSimulate[x][y].blockType = 0
                            mapToSimulate[x][y].move = False
                            mapToSimulate[x + 1][y + 1].blockType = 1
                    # water
                    elif mapToSimulate[x][y].blockType == 2:
                        if mapToSimulate[x][y + 1].blockType == 0:
                            mapToSimulate[x][y].blockType = 0
                            mapToSimulate[x][y].move = False
                            mapToSimulate[x][y + 1].blockType = 2
                        elif mapToSimulate[x][y + 1].blockType != 0 and mapToSimulate[x - 1][y + 1].blockType == 0 and \
                                mapToSimulate[x][y + 1].hard == False:
                            mapToSimulate[x][y].blockType = 0
                            mapToSimulate[x][y].move = False
                            mapToSimulate[x - 1][y + 1].blockType = 2
                        elif mapToSimulate[x][y + 1] != 0 and mapToSimulate[x + 1][y + 1].blockType == 0 and \
                                mapToSimulate[x][y + 1].hard == False:
                            mapToSimulate[x][y].blockType = 0
                            mapToSimulate[x][y].move = False
                            mapToSimulate[x + 1][y + 1].blockType = 2
                        elif mapToSimulate[x - 1][y].blockType == 0 and mapToSimulate[x + 1][y].blockType == 0:
                            mapToSimulate[x][y].blockType = 0
                            mapToSimulate[x][y].move = False
                            if bool(random.getrandbits(1)):
                                mapToSimulate[x - 1][y].blockType = 2
                            else:
                                mapToSimulate[x + 1][y].blockType = 2
                        elif mapToSimulate[x - 1][y].blockType != 0 and mapToSimulate[x + 1][y].blockType == 0:
                            mapToSimulate[x][y].blockType = 0
                            mapToSimulate[x][y].move = False
                            mapToSimulate[x + 1][y].blockType = 2
                        elif mapToSimulate[x - 1][y].blockType != 0 and mapToSimulate[x + 1][y].blockType != 0:
                            mapToSimulate[x][y].blockType = 2
                            mapToSimulate[x][y].move = False
            except IndexError:
                pass


def placeBlock(mapToPlace):
    mousex, mousey = pygame.mouse.get_pos()
    mousex = round(mousex / funny)
    mousey = round(mousey / funny)
    if mousex < mapX and mousey < mapY:
        mapToPlace[mousex][mousey].blockType = blockRn


def saveMap(mapToSave, mapID):
    b = {}
    b["world"] = []
    for x in range(0, mapX):
        for y in range(0, mapY):
            f = MyEncoder().encode(list({mapToSave[x][y]})).replace('[', '').replace(']', '')
            s = {'block': {'x': x, 'y': y}}
            s['block'].update(json.loads(f))
            b["world"].append(s)
    with open('worldSave/world1.json', 'w') as outfile:
        json.dump(b, outfile, indent=4)


def loadMap(mapJson, intoMap):
    myjsonfile = open('worldSave/'+mapJson)
    jsondata = myjsonfile.read()
    obj = json.loads(jsondata)
    for block in obj['world']:
        lol = block['block']
        funnyMap = intoMap[lol['x']][lol['y']]
        funnyMap.blockType = lol['blockType']
        funnyMap.liquid = lol['liquid']
        funnyMap.hard = lol['hard']


def playerFill():
    global player_rect, vertical_momentum, air_timer, moving_left, moving_right, gameMap, screen, blockColor, \
        mapX, mapY, funny
    playerSc.moving_right = moving_right
    playerSc.moving_left = moving_left
    # playerSc.vertical_momentum = vertical_momentum
    # playerSc.air_timer = air_timer
    playerSc.gameMap = gameMap
    playerSc.screen = screen
    playerSc.blockColor = blockColor
    playerSc.mapX = mapX
    playerSc.mapY = mapY
    playerSc.funny = funny
    playerSc.player_rect = player_rect
    moving_right = playerSc.moving_right
    moving_left = playerSc.moving_left
    # vertical_momentum = playerSc.vertical_momentum
    air_timer = playerSc.air_timer
    gameMap = playerSc.gameMap
    screen = playerSc.screen
    blockColor = playerSc.blockColor
    mapX = playerSc.mapX
    mapY = playerSc.mapY
    funny = playerSc.funny
    player_rect = playerSc.player_rect


# def collision_test(rect, tiles):
#     hit_list = []
#     for tile in tiles:
#         if rect.colliderect(tile):
#             hit_list.append(tile)
#     return hit_list
#
#
# def move(rect, movement, tiles):
#     collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
#     rect.x += movement[0]
#     hit_list = collision_test(rect, tiles)
#     for tile in hit_list:
#         if movement[0] > 0:
#             rect.right = tile.left
#             collision_types['right'] = True
#         elif movement[0] < 0:
#             rect.left = tile.right
#             collision_types['left'] = True
#     rect.y += movement[1]
#     hit_list = collision_test(rect, tiles)
#     for tile in hit_list:
#         if movement[1] > 0:
#             rect.bottom = tile.top
#             collision_types['bottom'] = True
#         elif movement[1] < 0:
#             rect.top = tile.bottom
#             collision_types['top'] = True
#     return rect, collision_types


gameMap = map_create()
placeOrSimulate = False

running = True
while running:
    screen.fill((50, 50, 50))
    pygame.draw.rect(screen, blockColor[0], (0, 0, mapX * funny, mapY * funny))
    # tile_rects = []
    # for x in range(round(player_rect.x / funny) - 2, round(player_rect.x / funny) + 2):
    #     for y in range(round(player_rect.y / funny) - 2, round(player_rect.y / funny) + 2):
    #         if gameMap[x][y].blockType != 0:
    #             tile_rects.append(pygame.Rect(x * funny, y * funny, funny, funny))
    # player_movement = [0, 0]
    # if moving_right == True:
    #     player_movement[0] += 2
    # if moving_left == True:
    #     player_movement[0] -= 2
    # player_movement[1] += vertical_momentum
    # vertical_momentum += 0.3
    # if vertical_momentum > 3:
    #     vertical_momentum = 3
    # player_rect, collisions = move(player_rect, player_movement, tile_rects)
    # if collisions['bottom'] == True:
    #     air_timer = 0
    #     vertical_momentum = 0
    # else:
    #     air_timer += 1
    # pygame.draw.rect(screen, blockColor[1], (player_rect.x, player_rect.y, 5, 13))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:
            placeBlock(gameMap)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                blockRn = 1
            if event.key == pygame.K_2:
                blockRn = 2
            if event.key == pygame.K_3:
                blockRn = 3
            if event.key == pygame.K_k:
                saveMap(gameMap, [0, 0])
            if event.key == pygame.K_l:
                loadMap("world1.json", gameMap)
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_SPACE:
                if air_timer < 6:
                    playerSc.vertical_momentum = -5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_a:
                moving_left = False
    draw_map(gameMap)
    playerFill()
    playerSc.playerdo()
    screen.blit(update_fps(), (10, 0))
    dt = clock.tick(100)
    clock.tick(100)
    time_elapsed_since_last_action += dt
    if time_elapsed_since_last_action > 250:
        check(gameMap)
        simulate(gameMap)
    pygame.display.update()
