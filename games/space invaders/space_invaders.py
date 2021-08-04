import pygame, random
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 155)
yellow = (255, 255, 0)

alien_ship_img = pygame.image.load('alien_ship.png')
space_ship_img = pygame.image.load('space_ship.png')
bullet_img = pygame.image.load('bullet.png')


display_width = 800
display_height = 600
FPS = 20

spaceship_height = 30
spaceship_width = 30

alien_width = 30
alien_height = 30

bullet_width = 5
bullet_height = 20

gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

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

def game_intro():
    intro = True
    gameDisplay.fill(white)
    message_to_screen("Welcome to Space Invaders", green, -150, "medium")
    message_to_screen("Aliens are invading Earth.", red, -100, "small")
    message_to_screen("You are Earth's last hope.", blue, -75, "small")
    message_to_screen("Destroy all aliens.", red, -50, "small")
    message_to_screen("Use arrows to control your ship.", black, -15, "small")
    message_to_screen("Press SPACE to shoot.", black, 10, "small")
    message_to_screen("Press C to play or Q to quit", black, 80, "medium")
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

    spaceshipX = display_width/2
    spaceshipY = display_height - spaceship_height
    
    spaceship_speed = 0
    bullet_speed = 10
    alien_hor_speed = 10
    alien_ver_speed = 45

    bullet_list = []
    alien_list = [[], [], []]
    bullets_to_delete = []
    aliens_to_delete = [[], [], []]

    motion = False

    for i in range(3):
        for j in range(int((display_width-20)/(alien_width+30))):
            alien_list[i].append([10+j*(alien_width+10), 20+i*(alien_height+5)])

    while not gameExit:

        if len(alien_list[0]) == 0 and len(alien_list[1]) == 0 and len(alien_list[2]) == 0:
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
                            pygame.quit()
                            quit()
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
                            pygame.quit()
                            quit()
                        elif event.key == pygame.K_c:
                            gameLoop()


        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_LEFT:
                    spaceship_speed = -10
                elif event.key == pygame.K_RIGHT:
                    spaceship_speed = 10
                elif event.key == pygame.K_SPACE:
                    bullet_list.append([spaceshipX+spaceship_width/2-4, spaceshipY-bullet_height])#4 is for error correction when image is used
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    spaceship_speed = 0

        spaceshipX += spaceship_speed

        if spaceshipX < 0:
            spaceshipX = 0
            spaceship_speed = 0
        elif spaceshipX > display_width-spaceship_width:
            spaceshipX = display_width-spaceship_width
            spaceship_speed = 0
        
        for bullet in bullet_list:
            if bullet[1] <= 0:
                bullets_to_delete.append(bullet)
            else:
                bullet[1] -= bullet_speed
                
        for bullet in bullet_list:
            for i in [0, 1, 2]:
                for alien in alien_list[i]:
                    if alien[0] < bullet[0] < alien[0]+alien_width and alien[1] <= bullet[1] <= alien[1]+alien_height:
                        aliens_to_delete[i].append(alien)
                        bullets_to_delete.append(bullet)

        for bullet in bullets_to_delete:
            if bullet in bullet_list:
                bullet_list.remove(bullet)

        for i in range(3):
            for alien in aliens_to_delete[i]:
                if alien in alien_list[i]:
                    alien_list[i].remove(alien)

        bullets_to_delete = []
        aliens_to_delete = [[], [], []]

        if motion:
            for i in range(3):
                for alien in alien_list[i]:
                    alien[1] += alien_ver_speed
                    alien[0] -= alien_hor_speed
            alien_hor_speed *= -1
            motion = False

        for i in range(3):
            for alien in alien_list[i]:
                if alien[0] <= 0 or alien[0]+alien_width >= display_width:
                    motion = True
                elif alien[1]+alien_height >= display_height - alien_ver_speed:
                    gameLose = True
                else:
                    alien[0] += alien_hor_speed
        
        gameDisplay.fill(blue)
        gameDisplay.blit(space_ship_img, [spaceshipX, spaceshipY])
        #pygame.draw.rect(gameDisplay, black, [spaceshipX, spaceshipY, spaceship_width, spaceship_height])
        for bullet in bullet_list:
            gameDisplay.blit(bullet_img, [bullet[0], bullet[1]])
            #pygame.draw.rect(gameDisplay, black, [bullet[0], bullet[1], bullet_width, bullet_height])
        for i in range(3):
            for alien in alien_list[i]:
                gameDisplay.blit(alien_ship_img, [alien[0], alien[1]])
                #pygame.draw.rect(gameDisplay, red, [alien[0], alien[1], alien_width, alien_height])  
        pygame.display.update()
        clock.tick(FPS)

game_intro()

