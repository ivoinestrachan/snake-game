import curses
import random
import time


def main(stdscr):
    # Initialize the screen
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # Lightning bolt color
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    snk_x = sw // 4
    snk_y = sh // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    apple_emoji = "\U0001F34E"
    lightning_emoji = "\U000026A1"
    foods = [[sh // 2, sw // 2]]
    w.addstr(foods[0][0], foods[0][1], apple_emoji, curses.color_pair(2))

    key = curses.KEY_RIGHT
    score = 0
    start_time = time.time()
    lightning_position = []

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        if (
            snake[0][0] in [0, sh] or
            snake[0][1] in [0, sw] or
            snake[0] in snake[1:]
        ):
            curses.endwin()
            print(f"Game Over! Your score: {score}")
            quit()

        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        if snake[0] in foods:
            score += 1
            foods.remove(snake[0])
            w.addstr(snake[0][0], snake[0][1],
                     apple_emoji, curses.color_pair(2))
        elif snake[0] == lightning_position:
            lightning_position = []
            w.timeout(50)
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        for segment in snake:
            w.addch(segment[0], segment[1],
                    curses.ACS_CKBOARD, curses.color_pair(1))

        if time.time() - start_time > 10 or not foods:
            start_time = time.time()
            while True:
                new_food = [random.randint(
                    1, sh - 1), random.randint(1, sw - 1)]
                if new_food not in snake and new_food not in foods:
                    foods.append(new_food)
                    w.addstr(new_food[0], new_food[1],
                             apple_emoji, curses.color_pair(2))
                    break

        if not lightning_position and time.time() - start_time > 5:
            while True:
                new_lightning = [random.randint(
                    1, sh - 1), random.randint(1, sw - 1)]
                if new_lightning not in snake and new_lightning not in foods:
                    lightning_position = new_lightning
                    w.addstr(
                        lightning_position[0], lightning_position[1], lightning_emoji, curses.color_pair(3))
                    break

        w.addstr(
            0, 0, f"Score: {score}", curses.color_pair(1))
        w.refresh()


curses.wrapper(main)
