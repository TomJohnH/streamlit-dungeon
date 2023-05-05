import game_config
import streamlit as st
from random import randrange


# ------------------------------------------------------------
#
#                MOVEMENT FUNCTIONS
#
# ------------------------------------------------------------


def character_can_move(level_matrix, tileset_movable, x, y):
    """
    This function checks if the move is "legal" for a character in a given level matrix.

    Args:
        level_matrix (numpy.ndarray): A 2D array representing the level grid.
        tileset_movable (list): A dictionary of tileset names and booleans representing the movability of each tile type in the level.
        x (int): The x-coordinate of the character's desired position.
        y (int): The y-coordinate of the character's desired position.

    Returns:
        bool: True if the character can move to the desired position, False otherwise.
    """

    is_movable = tileset_movable[level_matrix[x - 1, y - 1]]
    return is_movable or st.session_state["fly_mode"]


def squared_distance(x1, y1, x2, y2):
    """
    Calculate the squared distance between two points.

    Args:
        x1: The x-coordinate of the first point.
        y1: The y-coordinate of the first point.
        x2: The x-coordinate of the second point.
        y2: The y-coordinate of the second point.

    Returns:
        The squared distance between the two points.
    """
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

def distance_from_player(player, movable_object):
    """
    Calculate the squared distances between a player and a movable object
    for current position and four possible moves (left, right, up, down).

    Args:
        player: The player object with x and y attributes.
        movable_object: The movable object with x and y attributes.

    Returns:
        A tuple with the squared distances for current position, left, right, up, and down moves.
    """
    px, py = player.x, player.y
    mx, my = movable_object.x, movable_object.y
    
    distance = squared_distance(px, py, mx, my)
    distance_l = squared_distance(px + 1, py, mx, my)
    distance_r = squared_distance(px - 1, py, mx, my)
    distance_u = squared_distance(px, py + 1, mx, my)
    distance_d = squared_distance(px, py - 1, mx, my)
    
    return distance, distance_l, distance_r, distance_u, distance_d

# ------------------------------------------------------------
#
#                move to player modularization
#
# ------------------------------------------------------------

def get_move_index(player, movable_object):
    """
    Get the index of the move with the shortest distance to the player.

    Args:
        player (object): The player object containing its x and y coordinates.
        movable_object (object): The movable object containing its x and y coordinates.

    Returns:
        int: The index of the move with the shortest distance to the player.
    """
    distances = distance_from_player(player, movable_object)
    return distances.index(min(distances))


def move_object(movable_object, direction, distance):
    """
    Move the object in the given direction by the given distance.

    Args:
        movable_object (object): The object to be moved containing its x and y coordinates.
        direction (str): The direction to move the object in ("left", "right", "up", or "down").
        distance (int): The distance to move the object.
    """
    if direction == "left":
        movable_object.x -= distance
    elif direction == "right":
        movable_object.x += distance
    elif direction == "up":
        movable_object.y -= distance
    elif direction == "down":
        movable_object.y += distance


def is_valid_move(movable_object, direction):
    """
    Check if a move in the given direction is valid for the movable_object.

    Args:
        movable_object (object): The object to be moved containing its x and y coordinates.
        direction (str): The direction to check the move in ("left", "right", "up", or "down").

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    new_x = movable_object.x
    new_y = movable_object.y

    if direction == "left":
        new_x -= 1
    elif direction == "right":
        new_x += 1
    elif direction == "up":
        new_y -= 1
    elif direction == "down":
        new_y += 1

    return character_can_move(st.session_state["level"], game_config.tileset_movable, new_y, new_x)


def move_to_player(player, movable_object):
    """
    Move the movable_object towards the player or perform a random move based on a random probability.

    Args:
        player (object): The player object containing its x and y coordinates.
        movable_object (object): The movable object containing its x and y coordinates.
    """
    selected_move_index = get_move_index(player, movable_object)
    directions = {1: "left", 2: "right", 3: "up", 4: "down"}

    if randrange(10) < 5:
        direction = directions.get(selected_move_index)

        if direction and is_valid_move(movable_object, direction):
            move_object(movable_object, direction, 1)
    else:
        random_move(movable_object)

def random_move(movable_object):
    """
    Move the movable_object in a random direction.

    Args:
        movable_object (object): The movable object containing its x and y coordinates.
    """

    def random_direction():
        return ["right", "left", "down", "up"][randrange(4)]

    direction = random_direction()
    directions = {
        "right": (movable_object.y, movable_object.x + 1),
        "left": (movable_object.y, movable_object.x - 1),
        "down": (movable_object.y + 1, movable_object.x),
        "up": (movable_object.y - 1, movable_object.x),
    }

    new_y, new_x = directions[direction]

    if character_can_move(st.session_state["level"], game_config.tileset_movable, new_y, new_x):
        movable_object.y, movable_object.x = new_y, new_x

# ------------------------------------------------------------
#
#                INTERACTION FUNCTIONS
#
# ------------------------------------------------------------


def encounter(player, enemy):

    # if you encounter an enemy and enemy is alive
    # you will lose health but enemy will die
    # player = st.session_state["player"]

    if player.x == enemy.x and player.y == enemy.y and enemy.alive == True:
        damage = randrange(30)
        st.session_state["bubble_text"] = create_text_bubble_html(
            "OMG -" + str(damage) + "hp",
            player.x,
            player.y - 1,
        )
        player.hp = player.hp - damage
        enemy.alive = False
        if player.hp <= 0:
            player.alive = False


def treasures(player, treasure):

    # if you encounter treasure you will get gold

    if player.x == treasure.x and player.y == treasure.y and treasure.visible:
        gold = randrange(20)
        st.session_state["bubble_text"] = create_text_bubble_html(
            "yeah! +" + str(gold) + " g",
            player.x,
            player.y - 1,
        )
        treasure.visible = False
        player.gold = player.gold + gold


# ------------------------------------------------------------
#
#                RENDERING FUNCTIONS
#
# ------------------------------------------------------------

def level_renderer(df, game_objects):
    """
    The heart of graphical engine, More optimized version.

    Generates the HTML for rendering a game level based on a dataframe and game objects.

    :param df: A dataframe representing the game level grid, with each cell containing an index for the tileset.
    :param game_objects: A string containing the HTML for game objects to be added to the level.
    :return: A string with the generated HTML for the game level.
    """
    def generate_tile_html(tile, col, row):
        return f'<img src="{game_config.tileset[tile]}" style="grid-column-start: {col}; grid-row-start: {row};">'

    level_rows = [
        "".join(generate_tile_html(tile, j + 1, i + 1) for j, tile in enumerate(row))
        for i, row in enumerate(df)
    ]
    level_html = f'<div class="container"><div class="gamegrid">{" ".join(level_rows)}{game_objects}</div></div>'
    return level_html


def tile_html(src, x, y, z):

    # this little function provides html for additional layers

    return f"""<img src="{src}" style="grid-column-start: {x}; grid-row-start: {y}; grid-column-end:{z}">"""


def additional_layers_html(level_name, layer_name, coordinates="xy"):
    """
    Generate HTML for additional layer elements such as torches, boxes, and voids.

    Args:
        level_name (str): The name of the level for which the additional layers are to be generated.
        layer_name (str): The name of the layer within the level for which the additional layers are to be generated.
        coordinates (str, optional): The coordinate system to be used. Default is 'xy', which sets z = x.
                                      If set to 'xyz', the z-coordinate from the layer data will be used.

    Returns:
        str: The generated HTML string for the specified additional layer elements.
    """
    name = ""

    for layer_item in st.session_state.level_data[level_name][layer_name]:
        temp = st.session_state.level_data[level_name][layer_name][layer_item]

        # Set z-coordinate based on input
        z = temp["z"] if coordinates == "xyz" else temp["x"]

        name += tile_html(
            src=game_config.tileset[temp["text"]],
            x=temp["x"],
            y=temp["y"],
            z=z,
        )

    return name

# ------------------------------------------------------------
#
#                game objects functions
#
# ------------------------------------------------------------


def generate_monsters_html(monsters_list):
    """Generates HTML for monsters.

    Args:
        monsters_state (list): A list of monster objects from the session state

    Returns:
        str: The generated HTML string.
    """

    # Initialize an empty string for HTML content
    html_content = ""

    # Iterate through the list of monsters and append their HTML content if they are alive
    for monster in monsters_list:
        if monster.alive:
            html_content += monster.html
            
    return html_content


def generate_chests_html(chests_list):

    html_content = ""

    for chest in chests_list:
        if chest.visible:
            html_content += chest.html

    return html_content


# ------------------------------------------------------------
#
#                visual gimmicks
#
# ------------------------------------------------------------

def create_text_bubble_html(text, x, y):
    """Create an HTML text bubble with the given text and position.

    Args:
        text: A string representing the text to be displayed in the bubble.
        x: An integer representing the starting x position of the bubble.
        y: An integer representing the starting y position of the bubble.

    Returns:
        A string containing the HTML code for the text bubble.
    """
    return f"""
        <div class="container_text" style="position: relative; 
        grid-column-start: {x}; grid-row-start: {y}; grid-column-end: {x+4};">
            <img src="https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/message.png">
            <div style="position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%); font-size:0.875rem;">{text}</div>
        </div>
    """


def get_text_boxes(player_x, player_y, level_name):
    """Get the text bubble at the player's current position in the given level.

    Args:
        player_x: An integer representing the x position of the player.
        player_y: An integer representing the y position of the player.
        level_name: A string representing the name of the level.

    Returns:
        A string containing the HTML code for the text bubble at the player's position.
    """
    result = ""
    level_data = st.session_state.level_data.get(level_name, {})
    bubble_data = level_data.get("bubbles", {})
    for bubble_name, data in bubble_data.items():
        if data.get("x") == player_x and data.get("y") == player_y:
            result = create_text_bubble_html(data.get("text"), player_x, player_y - 1)

    if st.session_state.bubble_text:
        result = st.session_state.bubble_text
        st.session_state.bubble_text = ""

    return result