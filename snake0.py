# coding: utf8
import pygame, time, random
import ai_lib

print("**********************************************")
print("*                    Snake                   *")
print("*            Hell edition on Python          *")
print("**********************************************")
pygame.init()


def snake(block_size, snakeList):
    for XnY in snakeList:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])


def mts(msg, color, x, y):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x, y])


def check_win(score):
    if score >= 10:
        return 1
    else:
        return 0


# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
custom_c = (125, 20, 233)
custom_c_s = (125, 20, 100)
c_ab = custom_c

# display initilization
display_width = 400
display_height = 400
block_size = 25

# creating window
gameDisplay = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Snake: Hell edition")

font = pygame.font.SysFont(None, 25)

gameExit = False
# variables
eaten_b = 0
anti_wall = 1
# координаты головы змейки
lead_x = display_width / 2
lead_y = display_height / 2
# переменные, отвечающие за направление движения змейки
lead_x_change = 0
lead_y_change = 0

snakeList = []
snakeLength = 1
score = 0

appleX = round(random.randrange(0, display_width) / block_size) * block_size
appleY = round(random.randrange(0, display_height) / block_size) * block_size
ai_lib.plog("APPLE", "first apple created at "+str(appleX)+" "+str(appleY))

applebX = round(random.randrange(0, display_width) / block_size) * block_size
applebY = round(random.randrange(0, display_height) / block_size) * block_size
ai_lib.plog("APPLE", "first bonus apple created at "+str(applebX)+" "+str(applebY))


while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change = -block_size
                lead_y_change = 0
                ai_lib.plog("MOVE", "left")
            elif event.key == pygame.K_RIGHT:
                lead_x_change = block_size
                lead_y_change = 0
                ai_lib.plog("MOVE", "right")
            elif event.key == pygame.K_DOWN:
                lead_x_change = 0
                lead_y_change = +block_size
                ai_lib.plog("MOVE", "down")
            elif event.key == pygame.K_UP:
                lead_x_change = 0
                lead_y_change = -block_size
                ai_lib.plog("MOVE", "up")

    gameDisplay.fill(white)

    if lead_x >= display_width - block_size or lead_x < 0 or lead_y >= display_height - block_size or lead_y < 0:
        if anti_wall == 1:
            if lead_x <= 0:
                lead_x = 375
            if lead_x == display_width:
                lead_x = 0
            if lead_y <= 0:
                lead_y = 375
            if lead_y == display_height:
                lead_y = 0
        else:
            ai_lib.plog("GAME", "dead by wall")
            gameDisplay.fill(white)
            mts(''.join(["Game over! Score: ", str(score)]), black, 100, 200)
            pygame.display.update()
            time.sleep(0.5)
            gameExit = True

    lead_x += lead_x_change
    lead_y += lead_y_change
    snakeHead = [lead_x, lead_y]
    snakeList.append(snakeHead)
    if len(snakeList) > snakeLength:
        del snakeList[0]

    for eachSegment in snakeList[:-1]:
        if eachSegment == snakeHead:
            ai_lib.plog("GAME", "dead by snake")
            gameDisplay.fill(white)
            mts(''.join(["Game over! Score: ", str(score)]), black, 100, 200)
            pygame.display.update()
            gameExit = True
    if lead_x == appleX and lead_y == appleY:
        score += 1
        ai_lib.plog("APPLE", "destroyed at "+str(appleX)+" "+str(appleY))
        appleX = round(random.randrange(block_size, display_width - block_size + 1) / block_size) * block_size
        appleY = round(random.randrange(block_size, display_width - block_size + 1) / block_size) * block_size
        ai_lib.plog("APPLE", "created at "+str(appleX)+" "+str(appleY))
        snakeLength += 1
    if lead_x == applebX and lead_y == applebY:
        if eaten_b == 1:
            score += 3
            ai_lib.plog("APPLE_BONUS", "destroyed  at "+str(applebX)+" "+str(applebY))
            applebX = round(random.randrange(block_size, display_width - block_size + 1) / block_size) * block_size
            applebY = round(random.randrange(block_size, display_width - block_size + 1) / block_size) * block_size
            ai_lib.plog("APPLE_BONUS", "created at "+str(applebX)+" "+str(applebY))
            snakeLength += 3
            eaten_b = 0
            c_ab = custom_c
        else:
            c_ab = custom_c_s
            eaten_b = 1
    # отображение количества очков
    mts(''.join(["Score: ", str(score)]), black, 10, 10)
    # отображение яблока
    pygame.draw.rect(gameDisplay, red, [appleX, appleY, block_size, block_size])
    pygame.draw.rect(gameDisplay, c_ab, [applebX, applebY, block_size, block_size])
    # отображение змейки
    snake(block_size, snakeList)
    if check_win(score) == 1:
        ai_lib.plog("GAME", "win")
        gameDisplay.fill(white)
        mts("You Win! Score: "+str(score), black, 100, 200)
        time.sleep(1)
        gameExit = True
    pygame.display.update()
    pygame.time.delay(150)

pygame.quit()
