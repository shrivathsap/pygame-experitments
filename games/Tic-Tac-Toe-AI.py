import pygame, random, time
pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

display_width = 600
display_height = 600
FPS = 10

gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

cell_loc_list = []
cell_list = []
cell_size = 180
cell_display_size = 170
cell_margin = 30

for i in range(3):
    for j in range(3):
        cell_loc_list.append([cell_margin+i*cell_size, cell_margin+j*cell_size])

smallfont = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 25)
medfont = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 50)
largefont = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 80)

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, x, y, size = "large"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (x+cell_size/2), (y+cell_size/2)
    gameDisplay.blit(textSurf, textRect)

class cell:
    def __init__(self, x, y, text = "none"):
        self.x = x
        self.y = y
        self.text = text
        pygame.draw.rect(gameDisplay, red, [x, y, cell_display_size, cell_display_size])

    def player_move(self):
        message_to_screen("X", black, self.x, self.y)
        self.text = "X"

    def cpu_move(self):
        message_to_screen("O", black, self.x, self.y)
        self.text = "O"

for item in cell_loc_list:
    block = cell(item[0], item[1])
    cell_list.append(block)

victory_combination = [[cell_list[0], cell_list[1], cell_list[2]],
                       [cell_list[3], cell_list[4], cell_list[5]],
                       [cell_list[6], cell_list[7], cell_list[8]],
                       [cell_list[0], cell_list[3], cell_list[6]],
                       [cell_list[1], cell_list[4], cell_list[7]],
                       [cell_list[2], cell_list[5], cell_list[8]],
                       [cell_list[0], cell_list[4], cell_list[8]],
                       [cell_list[2], cell_list[4], cell_list[6]]]

def ai_choice():
    cell_found = False
    choice = None
    for combination in victory_combination:
        if combination[0].text == "O" and combination[1].text == "O" and combination[2].text == "none" and choice == None:
            cell_found = True
            choice = combination[2]
            break
        elif combination[0].text == "O" and combination[2].text == "O" and combination[1].text == "none" and choice == None:
            cell_found = True
            choice = combination[1]
            break
        elif combination[1].text == "O" and combination[2].text == "O" and combination[0].text == "none" and choice == None:
            cell_found = True
            choice = combination[0]
            break
        elif combination[0].text == "X" and combination[1].text == "X" and combination[2].text == "none" and choice == None:
            cell_found = True
            choice = combination[2]
            break
        elif combination[0].text == "X" and combination[2].text == "X" and combination[1].text == "none" and choice == None:
            cell_found = True
            choice = combination[1]
            break
        elif combination[1].text == "X" and combination[2].text == "X" and combination[0].text == "none" and choice == None:
            cell_found = True
            choice = combination[0]
            break

    if not cell_found:
        #print("random choice")
        choice = random.choice(cell_list)

    return choice

def ai_choice2():#ai_choice() blocks before winning if a blocking chance occurs before a winning oppurtunity in victory_combination
    possible_win = []#ai_choice2()lists possible oppurtunities and gives priority to winning over blocking over randomness
    possible_block = []
    for combination in victory_combination:
        if combination[0].text == "O" and combination[1].text == "O" and combination[2].text == "none":
            possible_win.append(combination[2])
        elif combination[0].text == "O" and combination[2].text == "O" and combination[1].text == "none":
            possible_win.append(combination[1])
        elif combination[1].text == "O" and combination[2].text == "O" and combination[0].text == "none":
            possible_win.append(combination[0])
        elif combination[0].text == "X" and combination[1].text == "X" and combination[2].text == "none":
            possible_block.append(combination[2])
        elif combination[0].text == "X" and combination[2].text == "X" and combination[1].text == "none":
            possible_block.append(combination[1])
        elif combination[1].text == "X" and combination[2].text == "X" and combination[0].text == "none":
            possible_block.append(combination[0])

    if len(possible_win) != 0:
        return random.choice(possible_win)
    elif len(possible_block) != 0:
        return random.choice(possible_block)
    else:
        return random.choice(cell_list)                       

def gameLoop():
    player = True
    victor = "none"
    while len(cell_list) != 0 and victor == "none":
        if player:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            current_position = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            for block in cell_list:
                if block.x < current_position[0] < block.x+cell_size and block.y < current_position[1] < block.y+cell_size and click[0] == 1:
                    block.player_move()
                    cell_list.remove(block)
                    player = False
                    break
        else:
            block = ai_choice2()
            #block = random.choice(cell_list)
            block.cpu_move()
            cell_list.remove(block)
            player = True

        for combination in victory_combination:
            if combination[0].text == "X" and combination[1].text == "X" and combination[2].text == "X":
                victor = "player"
            elif combination[0].text == "O" and combination[1].text == "O" and combination[2].text == "O":
                victor = "cpu"

        pygame.display.update()
        clock.tick(FPS)

    if victor == "none":
        print("Draw")
    elif victor == "player":
        print("Win")
    else:
        print("Lose")

    time.sleep(0.5)

    pygame.quit()
    quit()


gameLoop()

    
