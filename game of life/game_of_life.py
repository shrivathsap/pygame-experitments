import pygame
pygame.init()

alive = (255, 255, 0)
dead = (0, 0, 0)
white = (255, 255, 255)

display_width = 1500
display_height = 800

cell_size = 25
cell_display_size = 20

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Conway\'s Game Of Life')
clock = pygame.time.Clock()

cell_list = []

for i in range(0, display_height, cell_size):
    for j in range(0, display_width, cell_size):
        cell_list.append([j, i, dead])

def life_of_cell(cell):
    x = cell[0]
    y = cell[1]
    cell_count = 0
    n_list = [[x-cell_size, y-cell_size], [x, y-cell_size], [x+cell_size, y-cell_size],
              [x-cell_size, y],              [x+cell_size, y],
              [x-cell_size, y+cell_size], [x, y+cell_size], [x+cell_size, y+cell_size]]
##    for i in cell_list:                       THESE STEPS ARE COMPUTATIONALLY INTENSIVE
##        if [i[0], i[1]] in n_list:
##            #print(i)
##            if i[2] == alive:
##                cell_count += 1
    for neighbour in n_list:
        try:#to correct edge cases
            color = gameDisplay.get_at((neighbour[0], neighbour[1]))
            if color[0] == alive[0]:
                cell_count += 1
        except:
            pass

    #RULES:
    if cell_count < 2:
        return dead#returns status of cell in the next generation
    elif cell_count == 2 and cell[2] == alive:
        return alive
    elif cell_count == 2 and cell[2] == dead:
        return dead
    elif cell_count == 3:
        return alive
    elif cell_count > 3:
        return dead

def set_config():#to activate first generation using mouse
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for i in cell_list:
        if i[0] <= cur[0] < i[0]+cell_size and i[1] <= cur[1] < i[1]+cell_size and click[0] == 1:
            if i[2] == dead:
                i[2] = alive
            else:
                i[2] = dead
            #pygame.draw.circle(gameDisplay, i[2], (i[0], i[1]), cell_display_size/2)
            pygame.draw.rect(gameDisplay, i[2], [i[0], i[1], cell_display_size, cell_display_size])
    pygame.display.update()
    clock.tick(5)

def gameLoop():
    thriving = True
    configured= False

    while not configured:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    configured = True
        set_config()

    #print(life_of_cell([60, 20, dead]))
    #print(life_of_cell([40, 40, alive]))
    
    while thriving:
        to_live = []#those that are to live into the next generation
        to_die = []#those that are to die in the next generation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        for cell in cell_list:
            current_status = cell[2]
            new_status = life_of_cell(cell)
            if current_status == alive and new_status == alive:
                to_live.append(cell)
            elif current_status == alive and new_status == dead:
                to_die.append(cell)
            elif current_status == dead and new_status == alive:
                to_live.append(cell)
            else:
                to_die.append(cell)
        for cell in to_live:
            #pygame.draw.circle(gameDisplay, alive, (cell[0], cell[1]), cell_display_size/2)
            pygame.draw.rect(gameDisplay, alive, [cell[0], cell[1], cell_display_size, cell_display_size])
            cell[2] = alive#upgrading the status of cell in the next generation; without this line the screen will freeze in the current generation
        for cell in to_die:
            #pygame.draw.circle(gameDisplay, dead, (cell[0], cell[1]), cell_display_size/2)
            pygame.draw.rect(gameDisplay, dead, [cell[0], cell[1], cell_display_size, cell_display_size])
            cell[2] = dead
                        
        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    quit()


gameLoop()
