import pygame
pygame.init()

white = (255, 255, 255)
empty = (0, 0, 0)
electron_head = (0, 0, 255)
electron_tail = (255, 0, 0)
conductor = (255, 255, 0)

display_width = 1500
display_height = 800

cell_size = 25
cell_display_size = 20

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Wire World')
clock = pygame.time.Clock()

cell_list = []

for i in range(0, display_height, cell_size):
    for j in range(0, display_width, cell_size):
        cell_list.append([j, i, empty])

def state_of_cell(cell):
    color = gameDisplay.get_at((cell[0], cell[1]))
    if color[0] == empty[0] and color[1] == empty[1] and color[2] == empty[2]:
        return empty
    elif color[0] == electron_head[0] and color[1] == electron_head[1] and color[2] == electron_head[2]:
        return electron_tail
    elif color[0] == electron_tail[0] and color[1] == electron_tail[1] and color[2] == electron_tail[2]:
        return conductor
    else:
        x = cell[0]
        y = cell[1]
        cell_count = 0
        n_list = [[x-cell_size, y-cell_size], [x, y-cell_size], [x+cell_size, y-cell_size],
                  [x-cell_size, y],              [x+cell_size, y],
                  [x-cell_size, y+cell_size], [x, y+cell_size], [x+cell_size, y+cell_size]]
        for neighbour in n_list:
            try:#to correct edge cases
                color = gameDisplay.get_at((neighbour[0], neighbour[1]))
                if color[0] == electron_head[0] and color[1] == electron_head[1] and color[2] == electron_head[2]:
                    cell_count += 1
            except:
                pass

        #RULES:
        if cell_count == 1:
            return electron_head
        else:
            return conductor

def set_config():#to activate first generation using mouse
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for i in cell_list:
        if i[0] <= cur[0] < i[0]+cell_size and i[1] <= cur[1] < i[1]+cell_size and click[0] == 1:
            if i[2] == empty:
                i[2] = conductor
            elif i[2] == conductor:
                i[2] = electron_head
            elif i[2] == electron_head:
                i[2] = electron_tail
            else:
                i[2] = empty
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

    #print(life_of_cell([60, 20, empty]))
    #print(life_of_cell([40, 40, alive]))
    
    while thriving:
        empties = []
        conductors = []
        e_heads = []
        e_tails = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        for cell in cell_list:
            current_status = cell[2]
            new_status = state_of_cell(cell)
##            if current_status == empty and new_status == empty:
##                empties.append(cell)
##            elif current_status == electron_head and new_status == electron_head:
##                e_head.append(cell)
##            elif current_status == empty and new_status == alive:
##                to_live.append(cell)
##            else:
##                to_die.append(cell)
            if current_status == empty:
                empties.append(cell)
            elif current_status == electron_head:
                e_tails.append(cell)
            elif current_status == electron_tail:
                conductors.append(cell)
            elif current_status == conductor and new_status == conductor:
                conductors.append(cell)
            else:
                e_heads.append(cell)
        for cell in empties:
            #pygame.draw.circle(gameDisplay, alive, (cell[0], cell[1]), cell_display_size/2)
            pygame.draw.rect(gameDisplay, empty, [cell[0], cell[1], cell_display_size, cell_display_size])
            cell[2] = empty#upgrading the status of cell in the next generation; without this line the screen will freeze in the current generation
        for cell in e_heads:
            #pygame.draw.circle(gameDisplay, empty, (cell[0], cell[1]), cell_display_size/2)
            pygame.draw.rect(gameDisplay, electron_head, [cell[0], cell[1], cell_display_size, cell_display_size])
            cell[2] = electron_head
        for cell in e_tails:
            #pygame.draw.circle(gameDisplay, empty, (cell[0], cell[1]), cell_display_size/2)
            pygame.draw.rect(gameDisplay, electron_tail, [cell[0], cell[1], cell_display_size, cell_display_size])
            cell[2] = electron_tail
        for cell in conductors:
            #pygame.draw.circle(gameDisplay, empty, (cell[0], cell[1]), cell_display_size/2)
            pygame.draw.rect(gameDisplay, conductor, [cell[0], cell[1], cell_display_size, cell_display_size])
            cell[2] = conductor
                        
        pygame.display.update()
        clock.tick(5)

    pygame.quit()
    quit()


gameLoop()
