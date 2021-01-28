import turtle
import sys
import math
import random
import os
import getpass

def left():
    if pause_state is False:
        x = player.xcor()
        if x > -275:
            player.setx(x - 25)


def right():
    if pause_state is False:
        x = player.xcor()
        if x < 275:
            player.setx(x + 25)


def menu_up():
    if pause_state is True:
        menu_select.sety(65)


def menu_down():
    if pause_state is True:
        menu_select.sety(-35)


def menu_choice():
    global pause_state, quit_state
    if pause_state is True and menu_select.ycor() == 65:
        pause_state = False
        resume.clear()
        leave_game.clear()
        menu_select.hideturtle()
    if pause_state is True and menu_select.ycor() == -35:
        quit_state = True
        pause_state = False


def shoot():
    global shoot_state
    global fire_state
    if pause_state is False:
        shoot_state = True
        if fire_state is False:
            bullet.setx(player.xcor())
            bullet.sety(player.ycor())


def pause_game():
    global pause_state
    if pause_state is False:
        pause_state = True
    elif pause_state is True:
        pause_state = False
        resume.clear()
        leave_game.clear()
        menu_select.hideturtle()


def isCollision(t1, t2):
    distance = math.sqrt((t1.xcor() - t2.xcor()) ** 2 + (t1.ycor() - t2.ycor()) ** 2)
    if distance < 18:
        return True
    else:
        return False


def restartgame():
    print("Function is Running")
    space = f'C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\Space Invader.py'
    os.execl(space, *sys.argv)

if __name__ == "__main__":
    user = getpass.getuser()

    wn = turtle.Screen()
    wn.register_shape(f"C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\Player Ship.gif")
    wn.register_shape(f"C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\Space Invaders Background.gif")
    wn.register_shape(f"C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\Alien.gif")
    wn.register_shape(f"C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\Menu Select.gif")
    wn.bgpic(f"C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\Space Invaders Background.gif")
    wn.title("Space Invaders!")
    wn.setup(900, 600)


    border = turtle.Turtle()
    border.hideturtle()
    border.penup()
    border.pencolor("white")
    border.pensize(3)
    border.speed(0)
    border.goto(-300, -300)
    border.pendown()
    for n in range(4):
        border.forward(600)
        border.left(90)

    player = turtle.Turtle()
    player.penup()
    player.setheading(90)
    player.sety(-250)
    player.shape(f"C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\Player Ship.gif")
    player.speed(0)

    bullet = turtle.Turtle()
    bullet.penup()
    bullet.hideturtle()
    bullet.shape("square")
    bullet.color("yellow")
    bullet.shapesize(.5, .25)
    bullet.sety(-700)
    bullet.speed(0)

    wn.listen()
    wn.onkey(left, "Left")
    wn.onkey(right, "Right")
    wn.onkey(shoot, "space")
    wn.onkey(pause_game, "Escape")
    wn.onkey(menu_up, "Up")
    wn.onkey(menu_down, "Down")
    wn.onkey(menu_choice, "Return")

    number_of_enemies = 5

    enemies = []

    for i in range(number_of_enemies):
        enemies.append(turtle.Turtle())

    for enemy in enemies:
        enemy.penup()
        x = random.randint(-200, 200)
        y = random.randint(100, 250)
        enemy.goto(x, y)
        enemy.shape(f"C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\Alien.gif")
        enemy.speed(0)

    s = 0

    score = turtle.Turtle()
    score.hideturtle()
    score.pencolor('white')
    score.penup()
    score.speed(0)
    score.goto(-375, 275)
    score.write(f'Score: {s}', False, "center", ("Arial", 14))

    w = 1

    wave = turtle.Turtle()
    wave.hideturtle()
    wave.pencolor('white')
    wave.penup()
    wave.speed(0)
    wave.sety(275)
    wave.write(f'Wave {w}', False, 'center', ('Arial', 16))

    enemy_speed = 2
    shoot_state = False
    fire_state = False
    pause_state = False
    flash = False
    quit_state = False
    ne = number_of_enemies

    resume = turtle.Turtle()
    resume.hideturtle()
    resume.penup()
    resume.pencolor('white')
    resume.speed(0)
    resume.sety(50)

    leave_game = turtle.Turtle()
    leave_game.hideturtle()
    leave_game.penup()
    leave_game.pencolor('white')
    leave_game.speed(0)
    leave_game.sety(-50)

    menu_select = turtle.Turtle()
    menu_select.hideturtle()
    menu_select.shape(f'C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\Menu Select.gif')
    menu_select.penup()
    menu_select.pencolor('white')
    menu_select.speed(0)
    menu_select.sety(65)

    h_s = open(f'C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\High Score.txt')
    highscore = turtle.Turtle()
    highscore.speed(0)
    highscore.hideturtle()
    highscore.pencolor('white')
    highscore.penup()
    highscore.goto(-375, 250)
    for number in h_s:
        highscore.write(f'High Score: {int(number)}', False, "center", ("Arial", 14))
        hs = int(number)
    h_s.close()

    while quit_state == False:
        if pause_state is True:
            resume.write('Resume', False, 'center', ('Arial', 20))
            leave_game.write('Exit', False, 'center', ('Arial', 20))
            menu_select.showturtle()
            while pause_state is True:
                if flash is True:
                    for t in range(8000000):
                        continue
                    flash = False
                    menu_select.hideturtle()
                elif flash is False:
                    for t in range(8000000):
                        continue
                    flash = True
                    menu_select.showturtle()
        for enemy in enemies:
            enemy.setx(enemy.xcor() + enemy_speed)

            if enemy.xcor() > 280:
                for e in enemies:
                    e.sety(e.ycor() - 40)
                enemy_speed *= -1

            if enemy.xcor() < -280:
                for e in enemies:
                    e.sety(e.ycor() - 40)
                enemy_speed *= -1

            if isCollision(bullet, enemy) is True:
                shoot_state = False
                fire_state = False
                bullet.hideturtle()
                bullet.sety(-700)
                enemy.shape("blank")
                enemy.reset()
                enemies.remove(enemy)
                s += 10
                score.clear()
                score.write(f'Score: {s}', False, "center", ("Arial", 14))
                if s >= hs:
                    h_s = open(f'C:\\Users\\{user}\\OneDrive\\Documents\\PSU Class Files\\Computer Science\\Python\\Space Invaders\\High Score.txt', 'w')
                    hs = str(s)
                    h_s.write(f'{hs}\n')
                    h_s.close()
                    highscore.clear()
                    highscore.write(f'High Score: {hs}', False, "center", ('Arial', 14))
                    hs = int(s)
                ne -= 1

            for u in enemies:
                if u.ycor() < -250:
                    player.hideturtle()
                    bullet.hideturtle()
                    for l in enemies:
                        l.hideturtle()
                    game_over = turtle.Turtle()
                    game_over.hideturtle()
                    game_over.pencolor('white')
                    game_over.write("Game Over", False, "center", ("Arial", 70))
                    wn.onkey(restartgame, 'r')
                    break
        if ne == 0:
            number_of_enemies += 1
            ne = number_of_enemies
            w += 1
            wave.clear()
            wave.write(f'Wave {w}', False, 'center', ('Arial', 16))
            if enemy_speed > 0:
                enemy_speed += .2
            elif enemy_speed < 0:
                enemy_speed -= .2
            for i in range(number_of_enemies):
                enemies.append(turtle.Turtle())
            for enemy in enemies:
                enemy.penup()
                x = random.randint(-200, 200)
                y = random.randint(100, 250)
                enemy.goto(x, y)
                enemy.shape("Alien.gif")
                enemy.speed(0)
        if shoot_state is True:
            fire_state = True
            bullet.showturtle()
            bullet.sety(bullet.ycor() + 20)
            if bullet.ycor() > 300:
                shoot_state = False
                firestate = False
                bullet.hideturtle()
                bullet.sety(-700)
    wn.bye()
    quit()

    wn.mainloop()