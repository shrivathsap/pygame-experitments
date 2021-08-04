import pygame, random
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

b_red_img = pygame.image.load('b_red.png')
b_blue_img = pygame.image.load('b_blue.png')
b_yellow_img = pygame.image.load('b_yellow.png')
archer_img = pygame.image.load('archer.png')
arrow_img = pygame.image.load('arrow.png')
icon_img = pygame.image.load('archer_icon.png')

display_width = 1000
display_height = 700
FPS = 20

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_icon(icon_img)
clock = pygame.time.Clock()

archer_height = 100
archer_width = 50

arrow_width = 30
arrow_height = 10

balloon_width = 50
balloon_height = 50
balloon_margin = display_width - 200

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

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)

def info_to_screen(score, arrows):
    text1 = smallfont.render(" Score : " + str(score), True, black)
    text2 = smallfont.render("Arrows left : " + str(arrows), True, black)
    gameDisplay.blit(text1, [0,0])
    gameDisplay.blit(text2, [display_width-200,0])

def random_balloon_gen(ydisplace):
    colors = [red, blue, yellow]
    return random.randrange(balloon_margin, display_width - balloon_width, balloon_width), random.randrange(display_height, display_height + ydisplace, 100), random.choice(colors)

def game_intro():
    intro = True
    gameDisplay.fill(white)
    message_to_screen("Welcome to Archer", green, -150, "large")
    message_to_screen("Shoot the balloons to score", black, -100, "small")
    message_to_screen("Press C to play or Q to quit", black, 30, "medium")
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                    gameLoop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.display.update()
        clock.tick(5)

def gameLoop():
    gameDisplay.fill(white)
    
    gameExit = False
    gameWin = False
    gameLose = False

    archerX = 10
    archerY = display_height/2
    archer_speed = 0
    arrowX = archerX+archer_width
    arrowY = archerY+archer_height/2
    arrow_speed = 20
    balloon_speed = 5
    arrow_list=  []
    balloon_list = []

    number_of_arrows = 20
    number_of_balloons = 20
    score = 0
    point = 1

    for i in range(number_of_balloons):
        balloon_list.append(list(random_balloon_gen(1000)))

    while not gameExit:
        
        if number_of_arrows < 0:
            gameLose = True
        elif score == point*number_of_balloons:
            gameWin = True
            
        if gameWin == True:
            message_to_screen("You win :)", green, -50, "large")
            message_to_screen("Press C to play again, Q to quit", black, 50, "medium")
            pygame.display.update()

            while gameWin == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT :
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameExit = True
                            gameWin = False
                        elif event.key == pygame.K_c:
                            gameLoop()

        if gameLose == True:
            message_to_screen("You lose :(", red, -50, "large")
            message_to_screen("Press C to play again, Q to quit", black, 50, "medium")
            pygame.display.update()

            while gameLose == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT :
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameExit = True
                            gameLose = False
                        elif event.key == pygame.K_c:
                            gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_UP:
                    archer_speed = -10
                elif event.key == pygame.K_DOWN:
                    archer_speed = 10
                elif event.key == pygame.K_SPACE:
                    number_of_arrows -= 1
                    arrow_list.append([archerX, archerY+archer_height/2])

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    archer_speed = 0

        archerY += archer_speed
        
        for arrow in arrow_list:
            for balloon in balloon_list:
                if balloon[0]-arrow[0]-arrow_width <= 5 and 0<arrow[1]-balloon[1]<balloon_width:
                    score += point
                    balloon_list.remove(balloon)
            if arrow[0] > display_width:
                arrow_list.remove(arrow)
            else:
                arrow[0] += arrow_speed
        
        if archerY < 0 :
            archerY = 0
        elif archerY > display_height - archer_height:
            archerY = display_height - archer_height

        for balloon in balloon_list:
            if balloon[1] <= 0:
                new_balloon = random_balloon_gen(50)
                #balloon[0] = new_balloon[0]
                balloon[1] = new_balloon[1]
                #balloon[2] = new_balloon[2]
            else:
                balloon[1] -= balloon_speed

        
        gameDisplay.fill(white)
        gameDisplay.blit(archer_img, [archerX, archerY])
        #pygame.draw.rect(gameDisplay, red, [archerX, archerY, archer_width, archer_height])
        for arrow in arrow_list:
            gameDisplay.blit(arrow_img, [arrow[0], arrow[1]])
            #pygame.draw.rect(gameDisplay, green, [arrow[0], arrow[1], arrow_width, arrow_height])
        for balloon in balloon_list:
            if balloon[2] == red:
                gameDisplay.blit(b_red_img, [balloon[0], balloon[1]])
            elif balloon[2] == blue:
                gameDisplay.blit(b_blue_img, [balloon[0], balloon[1]])
            elif balloon[2] == yellow:
                gameDisplay.blit(b_yellow_img, [balloon[0], balloon[1]])
            
            #pygame.draw.rect(gameDisplay, balloon[2], [balloon[0], balloon[1], balloon_width, balloon_height])

                
        info_to_screen(score, number_of_arrows)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
