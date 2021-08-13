import random
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    print(f"All board data this turn: {data}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    board_height = data["board"]["height"]
    board_width = data["board"]["width"]

    if my_head["x"] == 0:
        remove("left", possible_moves)
    if my_head["y"] == 0:
        remove("down", possible_moves)
    if my_head["x"] == (board_width - 1):
        remove("right", possible_moves)
    if my_head["y"] == (board_height - 1):
        remove("up", possible_moves)

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body

    for square in my_body:
        if square["x"] == my_head["x"] and (square["y"] - my_head["y"]) == 1:
            remove("up", possible_moves)
        elif square["x"] == my_head["x"] and (square["y"] - my_head["y"]) == -1:
            remove("down", possible_moves)
        elif (square["x"] - my_head["x"]) == 1 and square["y"] == my_head["y"]:
            remove("right", possible_moves)
        elif (square["x"] - my_head["x"]) == -1 and square["y"] == my_head["y"]:
            remove("left", possible_moves)

    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake
    opponents = data["board"]["snakes"][1:]
    for opp in opponents:
        if {"x": my_head["x"], "y": (my_head["y"] + 1)} in opp["body"]:
            remove("up", possible_moves)
        if {"x": my_head["x"], "y": (my_head["y"] - 1)} in opp["body"]:
            remove("down", possible_moves)
        if {"x": (my_head["x"] + 1), "y": my_head["y"]} in opp["body"]:
            remove("right", possible_moves)
        if {"x": (my_head["x"] - 1), "y": my_head["y"]} in opp["body"]:
            remove("left", possible_moves)

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board
    food = data["board"]["food"]
    health = data["you"]["health"]
    length = data["you"]["length"]
    if health <= 20 and length < 11:
        closeFood = closestFood(my_head, food)
        if closeFood[0] == 1 and safe(opponents, closeFood[1]):
            move = directionToMove(my_head, closeFood[1])
            if move in possible_moves:
                return move
        else:
            point = closeFood[1]
            # moves towards the closest piece of food
            if point["x"] > my_head["x"]:
                remove("left", possible_moves)
            if point["x"] < my_head["x"]:
                remove("right", possible_moves)
            if point["y"] > my_head["y"]:
                remove("down", possible_moves)
            if point["y"] < my_head["y"]:
                remove("up", possible_moves)

    # Choose a random direction from the remaining possible_moves to move in, and then return that move

    # TODO: Explore new strategies for picking a move that are better than random

    # makes sure not to collide with itself in the future
    if ({"x": my_head["x"], "y": (my_head["y"] + 2)} in my_body):
        remove("up", possible_moves)
    if ({"x": my_head["x"], "y": (my_head["y"] - 2)} in my_body):
        remove("down", possible_moves)
    if ({"x": (my_head["x"] + 2), "y": my_head["y"]} in my_body):
        remove("right", possible_moves)
    if ({"x": (my_head["x"] - 2), "y": my_head["y"]} in my_body):
        remove("left", possible_moves)

    if len(possible_moves) > 1:
        # checks for head to heads

        if ("up" in possible_moves) and not safe(opponents, {"x": my_head["x"], "y": (my_head["y"] + 1)}):
            remove("up", possible_moves)
        if ("down" in possible_moves) and not safe(opponents, {"x": my_head["x"], "y": (my_head["y"] - 1)}):
            remove("down", possible_moves)
        if ("right" in possible_moves) and not safe(opponents, {"x": (my_head["x"] + 1), "y": my_head["y"]}):
            remove("right", possible_moves)
        if ("left" in possible_moves) and not safe(opponents, {"x": (my_head["x"] - 1), "y": my_head["y"]}):
                remove("left", possible_moves)

    # if len(possible_moves) > 1:
    #     # prevents getting stuck in a corner
    #     awayFromCorners(my_head, possible_moves, board_height, board_width)

    move = random.choice(possible_moves)

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move


def remove(move, possible_moves):
    if move in possible_moves:
        possible_moves.remove(move)


def getDistance(head, point):
    return abs(head["x"] - point["x"]) + abs(head["y"] - point["y"])


def closestFood(head, food):
    min = getDistance(head, food[0])
    point = food[0]
    for each in food:
        dist = getDistance(head, each)
        if dist < min:
            min = dist
            point = each
    return (min, point)


def safe(opponents, point):
    for snake in opponents:
        if ((abs(snake["head"]["x"] - point["x"]) == 1) and (snake["head"]["y"] == point["y"])) or \
                ((abs(snake["head"]["y"] - point["y"]) == 1) and (snake["head"]["x"] == point["x"])):
            return False
    return True


def directionToMove(head, point):
    if point["x"] == head["x"] and (point["y"] - head["y"]) == 1:
        return "up"
    elif point["x"] == head["x"] and (point["y"] - head["y"]) == -1:
        return "down"
    elif (point["x"] - head["x"]) == 1 and point["y"] == head["y"]:
        return "right"
    elif (point["x"] - head["x"]) == -1 and point["y"] == head["y"]:
        return "left"


def awayFromCorners(head, moves, height, width):
    if (head["x"] == 0 or head["x"] == width - 1) and (head["y"] > height - 1 - head["y"]):
        remove("up", moves)
    elif (head["x"] == 0 or head["x"] == width - 1) and (head["y"] < height - 1 - head["y"]):
        remove("down", moves)
    elif (head["y"] == 0 or head["y"] == height - 1) and (head["x"] > width - 1 - head["x"]):
        remove("right", moves)
    elif (head["y"] == 0 or head["y"] == height - 1) and (head["x"] < width - 1 - head["x"]):
        remove("left", moves)