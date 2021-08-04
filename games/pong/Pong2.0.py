import pygame, random
pygame.init()

pygame.display.set_caption("Pong 2.0")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

display_width = 800
display_height = 600
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
FPS = 30
paddleLength = 40
paddleBreadth = 10
ballRadius = 5

dist_between_paddle_and_wall = 10

playerStep = 10
cpuStep = 6

winScore = 100
points = 10

ball_speed = []

gameDisplay = pygame.display.set_mode((display_width, display_height))
gameDisplay.fill(white)
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()


smallfont = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 25)
medfont = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 50)
largefont = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 80)

def choose_speed():
    global ball_speed
    ball_speed = []#Clears previous speeds
    sx = random.randrange(5, 10)#magnitude
    sy = random.randrange(5, 10)
    vx = random.choice([sx, -1*sx])#direction
    vy = random.choice([sy, -1*sy])
    ball_speed.append(vx)
    ball_speed.append(vy)

def choose_dir(xcor, ycor, vx, vy):
    remaining_dist = display_width - xcor
    prediction = float(((remaining_dist-10)/abs(vx)))*(vy)#absolute vy is not needed as we want to know whether the ball is going up or down
    return prediction+ycor#prediction is distance from balls current position

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
    textRect.center = (display_width/2), (display_height/2)+y_displace#For messages in more than 1 line
    gameDisplay.blit(textSurf, textRect)

def score(score1, score2):
    text1 = smallfont.render(" Score : " + str(score1), True, black)
    text2 = smallfont.render("Score : " + str(score2), True, black)
    gameDisplay.blit(text1, [0,0])
    gameDisplay.blit(text2, [display_width-150,0])

def pause():
    paused = True
    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press C to continue or Q to quit.", black, 30)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(5)


def game_intro():
    intro = True
    gameDisplay.fill(white)
    message_to_screen("Welcome to Pong 2.0", green, -100, "large")
    message_to_screen("The objective of this game is to play ping pong.", black, -25, "small")
    message_to_screen("Your opponent is a trained AI.", red, 0, "small")
    message_to_screen("Press UP to move up and DOWN to move down.", black, 25, "small")
    message_to_screen("Score more than"+str(winScore)+" to win.", black, 50, "small")
    message_to_screen("Press C to play, Q to quit, P to pause.", blue, 180)
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                    gameLoop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.display.update()
        clock.tick(15)

def gameLoop():
    global ball_speed

    gameExit = False
    gameWin = False
    gameLose = False
    
    player_motion = 'NO'
    playerX = dist_between_paddle_and_wall
    playerY = display_height/2
    cpuX = display_width - dist_between_paddle_and_wall - paddleBreadth
    cpuY = display_height/2
    ballX = display_width/2
    ballY = display_height/2

    playerScore = 0
    cpuScore = 0

    choose_speed()

#-------------------------------------------------------------------------------------------------------------------------------------------------------
    while not gameExit:
        if gameWin == True:
            message_to_screen("You win :)", green, -50, "large")
            message_to_screen("Press C to play again, Q to quit", black, 50, "medium")
            pygame.display.update()

        while gameWin == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    gameExit = True
                    gameWin = False
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
                    gameExit = True
                    gameLose = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameLose = False
                    elif event.key == pygame.K_c:
                        gameLoop()
#--------------------------------------------------------------------------------------------------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_UP:
                    player_motion = 'UP'
                elif event.key == pygame.K_DOWN:
                    player_motion = 'DOWN'
                elif event.key == pygame.K_p:
                    pause()
            elif event.type == pygame.KEYUP:
                player_motion = 'NO'

        if player_motion == 'UP':
            if playerY>=playerStep:
                playerY -= playerStep
        elif player_motion == 'DOWN':
            if playerY<=display_height-playerStep-paddleLength:
                playerY += playerStep

        ballX += ball_speed[0]
        ballY += ball_speed[1]

        if ballY < ballRadius :
            ballY += 2*abs(ball_speed[1])
            ball_speed[1] *= -1
        elif ballY > display_height-ballRadius:
            ballY -= 2*abs(ball_speed[1])
            ball_speed[1] *= -1
        elif ballX <= playerX+paddleBreadth:
            if (ballY < playerY or ballY > playerY+paddleLength):
                cpuScore += points
                choose_speed()
                ballX, ballY = display_width/2, display_height/2
            else:
                ballX -= 2*(ball_speed[0])
                ball_speed[0] *= -1
        elif ballX >= cpuX :
            if (ballY < cpuY or ballY > cpuY+paddleLength):
                playerScore += points
                choose_speed()
                ballX, ballY = display_width/2, display_height/2
            else:
                ballX -= 2*(ball_speed[0])
                ball_speed[0] *= -1
            
        if ball_speed[0]>0:
            expectation = choose_dir(ballX, ballY, ball_speed[0], ball_speed[1])
            if expectation-cpuY >= paddleLength/2 and cpuY<=display_height-cpuStep-paddleLength:
                cpuY += cpuStep
            elif cpuY-expectation >= 0 and cpuY>=cpuStep:
                cpuY -= cpuStep

        if playerScore >= winScore:
            gameWin = True
        elif cpuScore >= winScore:
            gameLose = True
            
        gameDisplay.fill(white)
        score(playerScore, cpuScore)
        pygame.draw.rect(gameDisplay, blue, [playerX, playerY, paddleBreadth, paddleLength])
        pygame.draw.rect(gameDisplay, red, [cpuX, cpuY, paddleBreadth, paddleLength])
        pygame.draw.circle(gameDisplay, green, [int(ballX), int(ballY)], ballRadius)
        pygame.display.update()

        clock.tick(20)

    pygame.quit()
    quit()


game_intro()
