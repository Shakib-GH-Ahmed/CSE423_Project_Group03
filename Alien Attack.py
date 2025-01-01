from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Spaceship coordinates
spaceshipX = 250  # X-coordinate
spaceshipY = 50   # Y-coordinate


# Game variables
special_circle = [random.randint(100, 400), 720, 10]  # x, y, radius
radius_direction = 1  # Controls radius expansion/shrink
falling_circles = [[random.randint(100, 400), 480],
                   [random.randint(100, 400), 600]]
projectiles = []  # List to store projectile positions (x, y)
missed_fire = 0
pause = False
over = False
score = 0
count = 0
spaceship_health = 100
# Power-up agent variables
power_up_agent = [random.randint(100, 400), 500]  # Initial position
power_up_active = False  # Track if the power-up is active


# Boost-Up Agent variables
boost_up_agent = [random.randint(100, 400), 700]  # Initial position of the Boost-Up Agent
boost_up_active = False  # Track if the Boost-Up Agent is active

# Bomb variables
bomb = [random.randint(100, 400), 500]  # Initial position


heart = [random.randint(100, 400), 500]  # Initial position of the heart
skull = [random.randint(100, 400), 600]  # Initial position of the skull


# Midpoint Line Algorithm
def midpoint_line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    d = 2 * dy - dx
    y = y0

    glBegin(GL_POINTS)
    for x in range(x0, x1 + 1):
        glVertex2f(x, y)
        if d > 0:
            y += 1
            d -= 2 * dx
        d += 2 * dy
    glEnd()

# Midpoint Circle Algorithm
def midpoint_circle(x_center, y_center, radius):
    x = 0
    y = radius
    d = 1 - radius

    def draw_circle_points(xc, yc, x, y):
        draw_points(xc + x, yc + y)
        draw_points(xc - x, yc + y)
        draw_points(xc + x, yc - y)
        draw_points(xc - x, yc - y)
        draw_points(xc + y, yc + x)
        draw_points(xc - y, yc + x)
        draw_points(xc + y, yc - x)
        draw_points(xc - y, yc - x)

    draw_circle_points(x_center, y_center, x, y)
    while x < y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
        draw_circle_points(x_center, y_center, x, y)

# Draw the spaceship
def drawSpaceship():
    glPointSize(2.0)

    # Front Shooter
    glColor3f(1, 1, 1)  # White color
    midpoint_line(spaceshipX, spaceshipY + 20, spaceshipX, spaceshipY + 20)

    # Middle Body (Rectangle)
    glColor3f(0.137255, 0.419608, 0.556863)  # Blueish color
    for y in range(spaceshipY - 15, spaceshipY + 15):
        midpoint_line(spaceshipX - 20, y, spaceshipX + 20, y)

    # Design on Middle
    glColor3f(0.90, 0.91, 0.98)  # Light blueish color
    midpoint_line(spaceshipX - 10, spaceshipY - 5, spaceshipX - 10, spaceshipY - 5)
    midpoint_line(spaceshipX + 10, spaceshipY - 5, spaceshipX + 10, spaceshipY - 5)

    # Thrusters
    glColor3f(1, 1, 1)  # White color
    midpoint_line(spaceshipX - 10, spaceshipY - 20, spaceshipX - 10, spaceshipY - 15)
    midpoint_line(spaceshipX + 10, spaceshipY - 20, spaceshipX + 10, spaceshipY - 15)

    # Right Wing
    glColor3f(0.196078, 0.8, 0.196078)  # Green color
    for y in range(spaceshipY - 15, spaceshipY + 15):
        x_start = spaceshipX + 20
        x_end = spaceshipX + 20 + (15 - (y - (spaceshipY - 15)))
        midpoint_line(x_start, y, x_end, y)

    # Left Wing
    glColor3f(0.196078, 0.8, 0.196078)  # Green color
    for y in range(spaceshipY - 15, spaceshipY + 15):
        x_start = spaceshipX - 20
        x_end = spaceshipX - 20 - (15 - (y - (spaceshipY - 15)))
        midpoint_line(x_end, y, x_start, y)

    if not boost_up_active:
        # Up Body (Top Triangle)
        glColor3f(0.99609, 0.83984, 0)  # Yellow color
        for y in range(spaceshipY + 15, spaceshipY + 30):
            x_start = spaceshipX - (30 - y + spaceshipY)
            x_end = spaceshipX + (30 - y + spaceshipY)
            midpoint_line(x_start, y, x_end, y)
    else:
        glColor3f(0.99609, 0.83984, 0)  # Yellow color
        radius = 15  # Radius of the half-circle
        for y in range(spaceshipY + 15, spaceshipY + 30):
            x_offset = int((radius ** 2 - (y - (spaceshipY + 15)) ** 2) ** 0.5)
            x_start = spaceshipX - x_offset
            x_end = spaceshipX + x_offset
            midpoint_line(x_start, y, x_end, y)

# Draw a point
def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()



# Draw the Heart (+)
def draw_heart(x, y):
    # Draw the circular part of the Heart
    glColor3f(0.0, 1.0, 0.0)  # Green color
    for cy in range(y - 10, y + 10):
        x_start = int(x - (10 ** 2 - (cy - y) ** 2) ** 0.5)  # Circle equation
        x_end = int(x + (10 ** 2 - (cy - y) ** 2) ** 0.5)
        midpoint_line(x_start, cy, x_end, cy)

    #  "+" sign
    glColor3f(0.0, 0.0, 0.0)  # White color
    midpoint_line(x, y - 5, x, y + 5)  # Vertical line
    midpoint_line(x - 5, y, x + 5, y)  # Horizontal line


# Draw the Skull (-)
def draw_skull(x, y):
    # Draw the circular part of the Skull
    glColor3f(1.0, 0.0, 0.0)  # Red color
    for cy in range(y - 10, y + 10):
        x_start = int(x - (10 ** 2 - (cy - y) ** 2) ** 0.5)  # Circle equation
        x_end = int(x + (10 ** 2 - (cy - y) ** 2) ** 0.5)
        midpoint_line(x_start, cy, x_end, cy)

    # Draw the "-" sign
    glColor3f(1.0, 1.0, 1.0)  # White color
    midpoint_line(x - 5, y, x + 5, y)  # Horizontal line

    # Draw the eyes
    glColor3f(0.0, 0.0, 0.0)  # Black color
    midpoint_circle(x - 4, y + 4, 2)  # Left eye
    midpoint_circle(x + 4, y + 4, 2)  # Right eye

# Update life agents and check collisions
def update_life_agents():
    global heart, skull, spaceshipX, spaceshipY, spaceship_health, over

    # Move the Heart downward
    heart[1] -= 3  # Adjust speed as needed
    if heart[1] < 0:  # Reset position if it goes off the screen
        heart = [random.randint(100, 400), 500]

    # Check collision with spaceship (Heart)
    dx = heart[0] - spaceshipX
    dy = heart[1] - (spaceshipY + 15)  # Adjust for spaceship's middle position
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance < 20:# Collision detected
        if spaceship_health<=99:
            spaceship_health += 25  # Increase health
            if spaceship_health > 100:
                spaceship_health=100
            print(f"Health increased! Current health: {spaceship_health}")
            heart = [random.randint(100, 400), 500]  # Reset position

    # Move the Skull downward
    skull[1] -= 2  # Adjust speed as needed
    if skull[1] < 0:  # Reset position if it goes off the screen
        skull = [random.randint(100, 400), 600]

    # Check collision with spaceship (Skull)
    dx = skull[0] - spaceshipX
    dy = skull[1] - (spaceshipY + 15)  # Adjust for spaceship's middle position
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance < 20:  # Collision detected
        spaceship_health -= 34  # Decrease health
        if spaceship_health <=0:
            over = True
            print("Gamev over")
            print(f"Health decreased! Current health: {spaceship_health}")
        else:

            print(f"Health decreased! Current health: {spaceship_health}")
            skull = [random.randint(100, 400), 600]  # Reset position

# Draw the bomb

def draw_bomb():
    # Draw the circular part of the bomb (filled red)
    glColor3f(1.0, 0.0, 0.0)  # Bright red color
    for y in range(bomb[1] - 15, bomb[1] + 15):  # Filling the circle area with horizontal lines
        x_start = int(bomb[0] - (15 ** 2 - (y - bomb[1]) ** 2) ** 0.5)  # Circle equation x^2 + y^2 = r^2
        x_end = int(bomb[0] + (15 ** 2 - (y - bomb[1]) ** 2) ** 0.5)
        midpoint_line(x_start, y, x_end, y)

    # Draw the rectangular part of the bomb (filled red)
    glColor3f(1.0, 0.0, 0.0)  # Same red color for consistency
    for y in range(bomb[1] + 15, bomb[1] + 25):  # Start above the circle, filling upward
        midpoint_line(bomb[0] - 5, y, bomb[0] + 5, y)



# Update bomb position and check collision
# Update bomb position and check collision
# Update bomb position and check collision
def update_bomb():
    global bomb, bomb_active, spaceshipX, spaceshipY, spaceship_health, over

    # Move the bomb downward
    bomb[1] -= 1  # Adjust speed as needed
    if bomb[1] < 0:  # If the bomb goes off the screen, reset its position
        bomb = [random.randint(100, 400), 500]  # Deactivate bomb if it leaves the screen
    # Check collision with the spaceship
    dx = bomb[0] - spaceshipX
    dy = bomb[1] - (spaceshipY + 15)  # Adjust for the spaceship's middle position
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if distance < 30:  # Collision detected
        spaceship_health -= 100
        if spaceship_health <= 0:
            over = True
            print("Game Over!")
            clear_screen()



# Clear all elements from the screen
def clear_screen():
    global falling_circles, projectiles, special_circle, bomb, bomb_active
    falling_circles.clear()
    projectiles.clear()
    special_circle = [0, 0, 0]
    bomb_active = False

# Draw power-up agent
def draw_power_up_agent():
    glColor3f(0.0, 1.0, 1.0)  # Cyan for the agent
    midpoint_circle(power_up_agent[0], power_up_agent[1], 10)  # Outer circle
    glColor3f(1.0, 0.0, 0.0)  # Red for the missile inside
    midpoint_circle(power_up_agent[0], power_up_agent[1], 5)

# Update power-up agent position and check activation
def update_power_up_agent():
    global power_up_agent, power_up_active, spaceshipX, spaceshipY

    # Move the power-up agent downward
    power_up_agent[1] -= 1.5
    if power_up_agent[1] < 0:
        power_up_agent = [random.randint(100, 400), 500]  # Reset position if out of bounds

    # Check collision with spaceship
    dx = power_up_agent[0] - spaceshipX
    dy = power_up_agent[1] - (spaceshipY + 30)  # Adjust for spaceship's top position
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if not power_up_active:
        if distance < 20:  # Collision detected
            power_up_active = True
            print("Power-Up Activated!")



# Draw Boost-Up Agent
# Draw Boost-Up Agent
# Draw Boost-Up Agent
def draw_boost_up_agent():
    # Draw the thicker green circle (outer circle)
    glColor3f(0.0, 1.0, 0.0)  # Green color
    midpoint_circle(boost_up_agent[0], boost_up_agent[1], 15)  # Outer circle with increased radius

    # Draw three thicker dark red horizontal lines with increased spacing and thickness
    glColor3f(0.5, 0.0, 0.0)  # Dark red color
    for y_offset in [-1, 0, 1]:  # Spaced lines: Top (-8), Middle (0), Bottom (+8)
        for thickness in range(-3, 4):  # Make each line 7 units thick
            midpoint_line(
                boost_up_agent[0] - 15,  # Start point X (adjusted for larger radius)
                boost_up_agent[1] + y_offset + thickness,  # Adjusted Y for spacing and thickness
                boost_up_agent[0] + 15,  # End point X (adjusted for larger radius)
                boost_up_agent[1] + y_offset + thickness  # Same Y for thickness
            )


# Update Boost-Up Agent position and check activation
def update_boost_up_agent():
    global boost_up_agent, boost_up_active, spaceshipX, spaceshipY

    # Move the Boost-Up Agent downward
    boost_up_agent[1] -= 2
    if boost_up_agent[1] < 0:
        boost_up_agent = [random.randint(100, 400), 700]  # Reset position if out of bounds

    # Check collision with spaceship
    dx = boost_up_agent[0] - spaceshipX
    dy = boost_up_agent[1] - (spaceshipY + 30)  # Adjust for spaceship's top position
    distance = (dx ** 2 + dy ** 2) ** 0.5
    if not boost_up_active and distance < 25:  # Adjust collision range if needed
        boost_up_active = True
        print("Boost-Up Activated: Tri-Shot Mechanism Enabled!")



# Draw missiles (shorter rectangle with a triangular top)
def draw_missiles():
    global power_up_active
    for missile in projectiles[:]:
        # Change missile color if power-up is active
        if power_up_active:
            glColor3f(1.0, 1.0, 0.0)  # Yellow for enhanced missiles
        else:
            glColor3f(1.0, 0.0, 0.0)  # Red for normal missiles

        # Draw the missile body
        for y in range(missile[1], missile[1] + 30):
            midpoint_line(missile[0] - 5, y, missile[0] + 5, y)

        # Draw the missile tip
        for y in range(missile[1] + 30, missile[1] + 40):
            x_offset = y - (missile[1] + 30)
            midpoint_line(missile[0] - 5 + x_offset, y, missile[0] + 5 - x_offset, y)

        # Update missile position
        missile[1] += 3  # Central missile moves upward

        if missile[2] == 1:  # Top-right diagonal
            missile[0] += 1  # Adjust X-coordinate to move right
        elif missile[2] == -1:  # Top-left diagonal
            missile[0] -= 1  # Adjust X-coordinate to move left

        # Remove missile if it goes out of bounds
        if missile[1] > 500 or missile[0] < 0 or missile[0] > 500:
            projectiles.remove(missile)


# Draw falling circles
def draw_falling_circles():
    for circle in falling_circles:
        x, y = circle

        # Draw the UFO base (body)
        glColor3f(0.7, 0.7, 0.7)  # Gray color
        for i in range(5):
            midpoint_line(x - 15 + i, y - 5 + i, x + 15 - i, y - 5 + i)

        # Draw the circular body
        glColor3f(0.0, 1.0, 0.0)  # Green body
        midpoint_circle(x, y, 10)

        # Draw the dome
        glColor3f(0.5, 0.5, 1.0)  # Light blue dome
        for i in range(5):
            midpoint_line(x - 8 + i, y + 5 + i, x + 8 - i, y + 5 + i)

        # Add legs
        glColor3f(0.5, 0.3, 0.0)  # Brown legs
        midpoint_line(x - 10, y - 10, x - 15, y - 15)  # Left leg
        midpoint_line(x + 10, y - 10, x + 15, y - 15)  # Right leg

        # Add feet
        glColor3f(0.0, 0.0, 0.0)  # Black feet
        for i in range(3):
            midpoint_line(x - 17 + i, y - 16, x - 13 + i, y - 16)  # Left foot
            midpoint_line(x + 13 - i, y - 16, x + 17 - i, y - 16)  # Right foot

# Draw the special circle
def draw_special_circle():
    x, y, radius = special_circle

    # Draw the UFO base (special)
    glColor3f(1.0, 0.5, 0.0)  # Orange base
    for i in range(5):
        midpoint_line(x - radius - 5 + i, y - radius // 2 + i, x + radius + 5 - i, y - radius // 2 + i)

    # Draw the circular body
    glColor3f(0.0, 1.0, 0.0)  # Green body
    midpoint_circle(x, y, radius)

    # Draw the dome
    glColor3f(0.5, 0.5, 1.0)  # Light blue dome
    for i in range(5):
        midpoint_line(x - radius // 2 + i, y + radius + i, x + radius // 2 - i, y + radius + i)

    # Add legs
    glColor3f(0.5, 0.3, 0.0)  # Brown legs
    midpoint_line(x - radius, y - radius - 5, x - radius - 5, y - radius - 10)  # Left leg
    midpoint_line(x + radius, y - radius - 5, x + radius + 5, y - radius - 10)  # Right leg

    # Add feet
    glColor3f(0.0, 0.0, 0.0)  # Black feet
    for i in range(3):
        midpoint_line(x - radius - 7 + i, y - radius - 11, x - radius - 3 + i, y - radius - 11)  # Left foot
        midpoint_line(x + radius + 3 - i, y - radius - 11, x + radius + 7 - i, y - radius - 11)  # Right foot


# Animation logic
# Animation logic
def animation():
    global falling_circles, projectiles, special_circle, radius_direction, score, missed_fire

    if not pause and not over:
        # Move falling circles downward
        for circle in falling_circles:
            circle[1] -= 1
            if circle[1] < 0:
                circle[0] = random.randint(100, 400)
                circle[1] = 480

        # Move special circle downward and adjust radius
        special_circle[1] -= 1
        special_circle[2] += radius_direction
        if special_circle[2] > 20 or special_circle[2] < 5:
            radius_direction *= -1
        if special_circle[1] < 0:
            special_circle[0] = random.randint(100, 400)
            special_circle[1] = 480

        # Move missiles upward
        for missile in projectiles[:]:
            missile[1] += 3
            if missile[1] > 500:
                projectiles.remove(missile)


            # Check collisions with falling circles
            for circle in falling_circles[:]:
                dx = missile[0] - circle[0]
                dy = missile[1] - circle[1]
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < 15:
                    score += 1
                    print(f"Score: {score}")
                    falling_circles.remove(circle)
                    falling_circles.append([random.randint(100, 400), 480])
                    if not power_up_active:
                        projectiles.remove(missile)
                    break

            # Check for collision with special circle
            dx = missile[0] - special_circle[0]
            dy = missile[1] - special_circle[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance < special_circle[2] + 5:
                score += 3
                print(f"Score: {score}")
                special_circle[0] = random.randint(100, 400)
                special_circle[1] = 480
                special_circle[2] = 10
                if not power_up_active:
                    projectiles.remove(missile)

        # Update bomb position and check collision
        update_bomb()

        # Update power-up agent
        update_power_up_agent()

        # Update life agents
        update_life_agents()

        # Update Boost-Up Agent
        update_boost_up_agent()

        glutPostRedisplay()





def KeyboardListener(key, x, y):
    global spaceshipX, projectiles, boost_up_active
    if key == b'd' and spaceshipX < 480:
        spaceshipX += 10
    elif key == b'a' and spaceshipX > 20:
        spaceshipX -= 10
    elif key == b' ':
        if boost_up_active:
            # Fire three missiles when boost-up is active
            projectiles.append([spaceshipX, spaceshipY + 30, 0])  # Central missile
            projectiles.append([spaceshipX, spaceshipY + 30, 1])  # Top-right diagonal missile
            projectiles.append([spaceshipX, spaceshipY + 30, -1]) # Top-left diagonal missile
        else:
            # Fire a single missile
            projectiles.append([spaceshipX, spaceshipY + 30, 0])  # Central missile only
    glutPostRedisplay()



# Initialize OpenGL environment
def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Modify showScreen function to draw Boost-Up Agent
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    drawSpaceship()  # Draw the spaceship
    draw_missiles()  # Draw missiles
    draw_falling_circles()  # Draw falling circles
    draw_special_circle()  # Draw special circle
    draw_power_up_agent()  # Draw the power-up agent
    draw_boost_up_agent()  # Draw the Boost-Up Agent
    draw_bomb()  # Draw the bomb
    draw_heart(heart[0], heart[1])  # Draw the Heart (+)
    draw_skull(skull[0], skull[1])  # Draw the Skull (-)
    glutSwapBuffers()

# Initialize GLUT and start the main loop
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Spaceship Game with Power-Up Agent")
glutDisplayFunc(showScreen)
glutIdleFunc(animation)
glutKeyboardFunc(KeyboardListener)
glutMainLoop()
