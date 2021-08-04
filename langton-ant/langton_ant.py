import pygame
pygame.init()

#0->UP
#1->LEFT
#2->DOWN
#3->RIGHT

black = (255, 255, 255)
white = (0, 0, 0)
red = (255, 0, 0)

display_width = 1500
display_height = 800
FPS = 30

cell_size = 25
cell_display_size = 20
ant_size = 10

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Langton ant')
clock = pygame.time.Clock()

cell_list = []
current_pos = []

for i in range(0, display_height, cell_size):
    for j in range(0, display_width, cell_size):
        cell_list.append([j, i, white])

def direction(current_pos, direction):
    x = current_pos[0]
    y = current_pos[1]
    try:
        color = gameDisplay.get_at((x, y+ant_size+1))
        if color[0] == black[0]:
            if direction == 0:
                return 1
            elif direction == 1:
                return 2
            elif direction == 2:
                return 3
            else:
                return 0
        elif color[0] == white[0]:
            if direction == 0:
                return 3
            elif direction == 1:
                return 0
            elif direction == 2:
                return 1
            else:
                return 2
    except:
        pass

def set_config(ant_set):#to activate first generation using mouse
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if ant_set == 0 : 
        for i in cell_list:
            if i[0] <= cur[0] < i[0]+cell_size and i[1] <= cur[1] < i[1]+cell_size and click[0] == 1:
                if i[2] == black:
                    i[2] = white
                else:
                    i[2] = black
                pygame.draw.rect(gameDisplay, i[2], [i[0], i[1], cell_display_size, cell_display_size])
        pygame.display.update()
        clock.tick(5)
    else:
        for i in cell_list:
            if i[0] <= cur[0] < i[0]+cell_size and i[1] <= cur[1] < i[1]+cell_size and click[0] == 1:
                pygame.draw.rect(gameDisplay, red, [i[0], i[1], ant_size, ant_size])
                if len(current_pos) < 2:
                    current_pos.append(i[0])
                    current_pos.append(i[1])
        pygame.display.update()
        clock.tick(5)

def gameLoop():
    thriving = True
    configured= False
    ant_set = 0
    ant_direction = 0

    gameDisplay.fill(white)

    while not configured:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ant_set = 1
                if event.key == pygame.K_UP:
                    configured = True
        set_config(ant_set)
    
    while thriving:
        black_cells = []
        white_cells = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        ant_direction = direction(current_pos, ant_direction)
        cell_no = 0
        for i in range(len(cell_list)):
            cell = cell_list[i]
            if cell[0] == current_pos[0] and cell[1] == current_pos[1]:
                cell_no = i
                
        if cell_list[cell_no][2] == white:
            cell_list[cell_no][2] = black
        else:
            cell_list[cell_no][2] = white
            
        if ant_direction == 0:
            current_pos[1] -= cell_size
        elif ant_direction == 1:
            current_pos[0] -= cell_size
        elif ant_direction == 2:
            current_pos[1] += cell_size
        else:
            current_pos[0] += cell_size

        gameDisplay.fill(white)
        
        for cell in cell_list:
            pygame.draw.rect(gameDisplay, cell[2], [cell[0], cell[1], cell_display_size, cell_display_size])
        pygame.draw.rect(gameDisplay, red, [current_pos[0], current_pos[1], ant_size, ant_size])                
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


gameLoop()
