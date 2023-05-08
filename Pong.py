import turtle

# Set up the game window
wn = turtle.Screen()
wn.title("Pong by @Prat")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Function for getting player names
def get_player_names():
    # Get player A's name
    player_a_name = wn.textinput("Player A Name", "Enter Player A's name:")

    # Get player B's name
    player_b_name = wn.textinput("Player B Name", "Enter Player B's name:")

    return player_a_name, player_b_name

# Get player names
player_a_name, player_b_name = get_player_names()



# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(1)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = .25
ball.dy = .25

# Score variables
score_a = 0
score_b = 0

# Score display
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write(f"{player_a_name}: 0  {player_b_name}: 0", align="center", font=("Courier", 24, "normal"))


# Update the score display
# Update the score display
def update_score():
    score_display.clear()
    score_display.write(f"{player_a_name}: {score_a}  {player_b_name}: {score_b}", align="center", font=("Courier", 24, "normal"))


# Functions
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)

# Keyboard Binding
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(paddle_b_up, "Up")
wn.onkeypress(paddle_b_down, "Down")

# Main Game Loop
while True:
    wn.update()

    # Move Ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border Checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        # Player A scores
        score_a += 1
        update_score()

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        # Player B scores
        score_b += 1
        update_score()

    # Paddle and ball collisions
    if (ball.dx > 0) and (350 > ball.xcor() > 340) and (paddle_b.ycor() + 50 > ball.ycor() > paddle_b.ycor() - 50):
        ball.setx(340)
        ball.dx *= -1

    if (ball.dx < 0) and (-350 < ball.xcor() < -340) and (paddle_a.ycor() + 50 > ball.ycor() > paddle_a.ycor() - 50):
        ball.setx(-340)
        ball.dx *= -1

    # Game over
    if score_a >= 10:
        score_display.clear()
        score_display.write(f"GAME OVER - {player_a_name} wins!", align="center", font=("Courier", 24, "normal"))
        break

    if score_b >= 10:
        score_display.clear()
        score_display.write(f"GAME OVER - {player_b_name} wins!", align="center", font=("Courier", 24, "normal"))
        break


    
    # Game over
    if score_a >= 7:
        score_display.clear()
        score_display.write("GAME OVER - Player A wins!", align="center", font=("Courier", 24, "normal"))
        wn.mainloop()
        break

    if score_b >= 7:
        score_display.clear()
        score_display.write("GAME OVER - Player B wins!", align="center", font=("Courier", 24, "normal"))
        wn.mainloop()
        break


