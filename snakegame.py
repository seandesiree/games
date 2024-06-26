
import curses
from random import randint

def main(win):
    # Setting up a new window with 20 rows, 60 columns, starting at the top-left of the screen
    win = curses.newwin(20, 60, 0, 0) 

    # Configuring the window
    win.keypad(1)       # Enable keypad mode to capture key presses
    curses.noecho()     # Turn off automatic echoing of keys to the window
    curses.curs_set(0)  # Make the cursor invisible
    win.border(0)       # Draw a border around the window
    win.nodelay(1)      # Make getch() non-blocking

    # Initializing the snake and food
    snake = [(4, 10), (4, 9), (4, 8)]  # Starting coordinates of the snake
    food = (10, 20)  # Coordinates of the first food item
    bounds_y=(0,19)
    bounds_x=(0,59)
    # Set of allowed movement keys (arrow keys)
    allowed_moves = (curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN)

    # Mapping of each move to its opposite
    opposite_moves = {
        curses.KEY_LEFT: curses.KEY_RIGHT,
        curses.KEY_RIGHT: curses.KEY_LEFT,
        curses.KEY_UP: curses.KEY_DOWN,
        curses.KEY_DOWN: curses.KEY_UP
    }

    # Placing the first food item on the screen
    win.addch(food[0], food[1], 'O')

    # Game logic setup
    score = 0  # Initialize score
    ESC = 27   # ASCII value of the Escape key
    key = curses.KEY_RIGHT  # Initial movement direction of the snake

    try:
        while key != ESC:
            # Displaying the score at the top of the window
            win.addstr(0, 2, 'Score: ' + str(score) + ' ')

            # Setting the speed of the game
            win.timeout(150 - (len(snake)) // 5 + len(snake) // 10 % 120)

            prev_key = key       # Store the previous key pressed
            event = win.getch()  # Get the current key pressed
            key = event if event in allowed_moves else prev_key  # Update key if it's an allowed move

            # Checking if the new key is not the opposite of the previous key
            if event in allowed_moves:
                if opposite_moves[key] != prev_key:
                    key = event
                else:
                    key = prev_key

            # Calculating the new head position of the snake
            y = snake[0][0]
            x = snake[0][1]
            if key == curses.KEY_DOWN:
                y += 1
            if key == curses.KEY_UP:
                y -= 1
            if key == curses.KEY_LEFT:
                x -= 1
            if key == curses.KEY_RIGHT:
                x += 1

            # Inserting the new head position of the snake
            snake.insert(0, (y, x))

            # Checking for collisions with the border or the snake itself
            if y in bounds_y or x in bounds_x or snake[0] in snake[1:]:
                print(f"Game Over, Your Score was {score}")
                break  # End the game if a collision occurs

            # Checking if the snake has gotten the food
            if snake[0] == food:
                score += 1  # Increase score
                # Generate new food position
                food = ()
                while food == ():
                    food = (randint(bounds_y[0]+1,bounds_y[1]-1), randint(bounds_x[0]+1,bounds_x[1]-1))
                    if food in snake:
                        food = ()
                win.addch(food[0], food[1], 'O')  # Place new food
            else:
                # Moving the snake
                last = snake.pop()  # Remove the last segment of the snake
                win.addch(last[0], last[1], ' ')  # Clear the last segment from the screen

            # Drawing the new head of the snake
            win.addch(snake[0][0], snake[0][1], 'S')

    except Exception as e:
        print("error", e)

curses.wrapper(main)
