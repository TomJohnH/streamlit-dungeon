import game_config
import game_js
import json
import numpy as np
import pandas as pd
import random
from random import randrange
import streamlit as st
import streamlit.components.v1 as components
import time


# -------------- refrence docs: --------------

# https://www.pythonmorsels.com/making-auto-updating-attribute/
# https://developer.mozilla.org/en-US/docs/Games/Techniques/Tilemaps

# ------------------------------------------------------------
#
#                  Visual settings and functions
#
# ------------------------------------------------------------

st.set_page_config(
    page_title="The Dungeon", page_icon="🗡️", initial_sidebar_state="collapsed"
)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ------------------------------------------------------------
#
#                        Classes
#
# ------------------------------------------------------------

# object constructor for player and monsters


class Character:
    def __init__(self, x, y, file, hp, gold, alive):
        self.x = x
        self.y = y
        self.file = (
            "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/"
            + file
        )
        self.hp = hp
        self.gold = gold
        self.alive = alive

    @property
    def html(self):
        return (
            "<img src='"
            + str(self.file)
            + "' style='grid-column-start: "
            + str(self.x)
            + "; grid-row-start: "
            + str(self.y)
            + ";'>"
        )


# object constructor for chests and other inanimate objects


class InanimateObject:
    def __init__(self, x, y, file, visible):
        self.x = x
        self.y = y
        self.file = (
            "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/tileset/"
            + file
        )
        self.visible = visible

    @property
    def html(self):
        return (
            "<img src='"
            + str(self.file)
            + "' style='grid-column-start: "
            + str(self.x)
            + "; grid-row-start: "
            + str(self.y)
            + ";'>"
        )


# ------------------------------------------------------------
#
#                        Objects
#
# ------------------------------------------------------------


# ------------------------------------------------------------
#
#                  Variables and constants
#
# ------------------------------------------------------------

# ---------------- initiat session states ----------------

if "left_clicked" not in st.session_state:
    st.session_state["left_clicked"] = False

if "right_clicked" not in st.session_state:
    st.session_state["right_clicked"] = False

if "up_clicked" not in st.session_state:
    st.session_state["up_clicked"] = False

if "down_clicked" not in st.session_state:
    st.session_state["down_clicked"] = False

if "steps" not in st.session_state:
    st.session_state["steps"] = 0

if "bubble_text" not in st.session_state:
    st.session_state["bubble_text"] = ""

if "cold_start" not in st.session_state:
    st.session_state["cold_start"] = True

if "end" not in st.session_state:
    st.session_state["end"] = False


# ---------------- links ----------------

cat = "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/cat.gif"
player = "https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/player.gif"

# ------------------------------------------------------------
#
#                        Callbacks
#
# ------------------------------------------------------------


def left_callback():

    if character_can_move(
        st.session_state[
            "level"
        ],  # note the different order of x and y. Done to confuse myself in the future.
        # good luck future me
        st.session_state["player"].y,
        st.session_state["player"].x - 1,
    ):
        st.session_state["player"].x -= 1
        st.session_state.left_clicked = True
        st.session_state["steps"] += 1

    # this little loop is responsible for moving the monsters and reacting to encounters
    for i in range(0, len(st.session_state["monsters"])):
        random_move(st.session_state["monsters"][i])
        encounter(st.session_state["player"], st.session_state["monsters"][i])
    for i in range(0, len(st.session_state["chests"])):
        treasures(st.session_state["player"], st.session_state["chests"][i])


def right_callback():
    # player movement
    if character_can_move(
        st.session_state["level"],
        st.session_state["player"].y,
        st.session_state["player"].x + 1,
    ):
        st.session_state["player"].x += 1
        st.session_state.right_clicked = True
        st.session_state["steps"] += 1

    for i in range(0, len(st.session_state["monsters"])):
        random_move(st.session_state["monsters"][i])
        encounter(st.session_state["player"], st.session_state["monsters"][i])
    for i in range(0, len(st.session_state["chests"])):
        treasures(st.session_state["player"], st.session_state["chests"][i])


def up_callback():
    if character_can_move(
        st.session_state["level"],
        st.session_state["player"].y - 1,
        st.session_state["player"].x,
    ):
        st.session_state["player"].y -= 1
        st.session_state.up_clicked = True
        st.session_state["steps"] += 1

    for i in range(0, len(st.session_state["monsters"])):
        random_move(st.session_state["monsters"][i])
        encounter(st.session_state["player"], st.session_state["monsters"][i])
    for i in range(0, len(st.session_state["chests"])):
        treasures(st.session_state["player"], st.session_state["chests"][i])


def down_callback():
    if character_can_move(
        st.session_state["level"],
        st.session_state["player"].y + 1,
        st.session_state["player"].x,
    ):
        st.session_state["player"].y += 1
        st.session_state.down_clicked = True
        st.session_state["steps"] += 1

    for i in range(0, len(st.session_state["monsters"])):
        random_move(st.session_state["monsters"][i])
        encounter(st.session_state["player"], st.session_state["monsters"][i])
    for i in range(0, len(st.session_state["chests"])):
        treasures(st.session_state["player"], st.session_state["chests"][i])


# ------------------------------------------------------------
#
#                        Functions
#
# ------------------------------------------------------------


# ---------------- data fetch ----------------


@st.cache_data
def fetch_data(level_name):
    df = pd.read_csv(level_name, sep=",", header=None)
    return df


# ---------------- check surroundings ----------------

# this function checks all potential moves


def character_can_move(logic_layer, x, y):
    if tileset_movable[logic_layer[x - 1, y - 1]] == True:
        return True
    else:
        pass


# ---------------- random moves ----------------


def random_move(movable_object):

    # this function is responsible for random movement of monsters
    # it will be changed in the future - monsters will follow the player
    # is it possible? yes. check https://rogue-rpg.streamlit.app/

    rnd_move = randrange(100)
    # st.write("random_move" + str(rnd_move))
    if rnd_move < 25:
        if character_can_move(
            st.session_state["level"],
            movable_object.y,
            movable_object.x + 1,
        ):
            movable_object.x += 1
    if rnd_move >= 25 and rnd_move < 50:
        if character_can_move(
            st.session_state["level"],
            movable_object.y,
            movable_object.x - 1,
        ):
            movable_object.x -= 1
    if rnd_move >= 50 and rnd_move < 75:
        if character_can_move(
            st.session_state["level"],
            movable_object.y + 1,
            movable_object.x,
        ):
            movable_object.y += 1
    if rnd_move >= 75 and rnd_move < 100:
        if character_can_move(
            st.session_state["level"],
            movable_object.y - 1,
            movable_object.x,
        ):
            movable_object.y -= 1


# ---------------- encounter with monster ----------------


def encounter(player, enemy):

    # if you encounter an enemy and enemy is alive
    # you will lose health but enemy will die
    # player = st.session_state["player"]

    if player.x == enemy.x and player.y == enemy.y and enemy.alive == True:
        damage = randrange(30)
        st.session_state["bubble_text"] = text_bubble_html(
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
        st.session_state["bubble_text"] = text_bubble_html(
            "yeah! +" + str(gold) + " g",
            player.x,
            player.y - 1,
        )
        treasure.visible = False
        player.gold = player.gold + gold


# ------------------------------------------------------------
#
#                        Graphics engine
#
# ------------------------------------------------------------

# ---------------- CSS ----------------

local_css("style.css")

# ---------------- tilset dictionary ----------------

tileset = game_config.tileset

tileset_movable = game_config.tileset_movable

# ---------------- level renderer ----------------

# this is the heart of graphical engine
# whole game is based on a grid div with x & y columns
# placement of objects is done by manipulating grid-column-start: & grid-row-start:


def level_renderer(df, game_objects):
    i = 0
    j = 0
    level_html = '<div class="container"><div class="gamegrid">'
    for x in df:  # array from data frame: df.values
        # st.write(x)
        j = 0
        for y in x:

            # if y == "FP" and random.uniform(0, 1) > 0.7:
            #     tilset_tile = tileset["DK"]
            # else:
            #     tilset_tile = tileset[y]

            level_html = (
                level_html
                + '<img src="'
                + tileset[y]  # tilset_tile
                + '" style="grid-column-start: '
                + str(j + 1)
                + "; grid-row-start: "
                + str(i + 1)
                + ';">'
            )
            j = j + 1
        i = i + 1
    level_html = level_html + game_objects + "</div></div>"
    return level_html


# ------------------------------------------------------------
#
#             Game enigne - frontend html creator
#
# ------------------------------------------------------------

# --------------- level config ------------------------


if "level_data" not in st.session_state:
    level_config = game_config.level_config
    st.session_state.level_data = json.loads(level_config)

# ---------------- creating player html ----------------

if "player" not in st.session_state:
    ply = st.session_state.level_data["players_stats"]
    ply_xy = st.session_state.level_data["level1"]["player_xy"]
    st.session_state["player"] = Character(
        x=ply_xy["x"],
        y=ply_xy["y"],
        file=ply["file"],
        hp=ply["hp"],
        gold=ply["gold"],
        alive=ply["alive"],
    )

player = f"""
<img src="{player}" id="player" class="player" style="grid-column-start: {st.session_state["player"].x}; grid-row-start: {st.session_state["player"].y};">"""

# ---------------- creating monsters html ----------------

# we are constructing monsters in iteractions based on level configuration
if "monsters" not in st.session_state:
    st.session_state["monsters"] = []
    for i in range(0, len(st.session_state.level_data["level1"]["monsters"])):
        mst = list(st.session_state.level_data["level1"]["monsters"].values())[i]
        st.session_state["monsters"].append(
            Character(
                x=mst["x"],
                y=mst["y"],
                file=mst["file"],
                hp=mst["hp"],
                gold=mst["gold"],
                alive=mst["alive"],
            )
        )

# we are creating monsters html


def enemies_html(monsters_session_state):
    # empty string
    html = ""
    # creating html
    for i in range(0, len(monsters_session_state)):
        if monsters_session_state[i].alive:
            html = html + monsters_session_state[i].html
    # adding a cat - don't ask why
    html = (
        html
        + f"""
            <img src="{cat}" style="grid-column-start: 47; grid-row-start: 11;">
        """
    )
    return html


enemies = enemies_html(st.session_state["monsters"])

# ---------------- creating non interactive visual layers ----------------

# this little function provides html for additional layers
def tile_html(text, x, y, z):
    return f"""<img src="{text}" style="grid-column-start: {x}; grid-row-start: {y}; grid-column-end:{z}">"""


def additional_layers_html(level_name, layer_name, coordinates="xy"):
    name = ""
    for i in range(0, len(st.session_state.level_data[level_name][layer_name])):
        ob = list(st.session_state.level_data[level_name][layer_name].values())[i]
        if coordinates == "xyz":
            name = name + tile_html(
                text=tileset[ob["text"]], x=ob["x"], y=ob["y"], z=ob["z"]
            )
        else:
            name = name + tile_html(
                text=tileset[ob["text"]], x=ob["x"], y=ob["y"], z=ob["x"]
            )
    return name


# ---------------- boxes ----------------

if "boxes" not in st.session_state:
    st.session_state["boxes"] = additional_layers_html("level1", "boxes")

boxes = st.session_state["boxes"]

# ---------------- voids ----------------

if "voids" not in st.session_state:
    st.session_state["voids"] = additional_layers_html("level1", "voids", "xyz")

voids = st.session_state["voids"]

# ---------------- troches ----------------

if "torches" not in st.session_state:
    st.session_state["torches"] = additional_layers_html("level1", "torches")

torches = st.session_state["torches"]

# ---------------- TO BE REFACTORED ----------------

# we are constructing monsters in iteractions based on level configuration
if "chests" not in st.session_state:
    st.session_state["chests"] = []
    for i in range(0, len(st.session_state.level_data["level1"]["chests"])):
        chs = list(st.session_state.level_data["level1"]["chests"].values())[i]
        st.session_state["chests"].append(
            InanimateObject(
                x=chs["x"],
                y=chs["y"],
                file=chs["file"],
                visible=chs["visible"],
            )
        )


def chests_html(chests_ss_st):
    # empty string
    html = ""
    # creating html
    for i in range(0, len(chests_ss_st)):
        if chests_ss_st[i].visible:
            html = html + chests_ss_st[i].html
    # adding a cat - don't ask why
    html = (
        html
        + f"""
            <img src="{cat}" style="grid-column-start: 47; grid-row-start: 11;">
        """
    )
    return html


chests = chests_html(st.session_state["chests"])

# ---------------- creating visual layers textboxes ----------------


def text_bubble_html(text, x, y):
    return f"""<div class="container_text" style="position: relative; grid-column-start: {x}; grid-row-start: {y}; grid-column-end: {x+4};"><img src="https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/message.png"><div style="position: absolute; top: 40%;left: 50%;transform: translate(-50%, -50%);font-size:0.875rem;">{text}</div></div>"""


if st.session_state["player"].x == 10 and st.session_state["player"].y == 5:
    # text_boxes = f"""<div class="container_text" style="position: relative; grid-column-start: 10; grid-row-start: 4; grid-column-end: 14;"><img src="https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/message.png"><div style="position: absolute; top: 40%;left: 50%;transform: translate(-50%, -50%);">What?</div></div>"""
    text_boxes = text_bubble_html("What?", 10, 4)
elif st.session_state["player"].x == 16 and st.session_state["player"].y == 11:
    text_boxes = text_bubble_html("Strange", 16, 10)
elif st.session_state["player"].x == 5 and st.session_state["player"].y == 21:
    text_boxes = text_bubble_html("Monsters?", 5, 20)
elif st.session_state["player"].x == 47 and st.session_state["player"].y == 12:
    text_boxes = text_bubble_html("Meow!", 48, 10)
elif st.session_state["player"].x == 4 and st.session_state["player"].y == 17:
    text_boxes = text_bubble_html("box (ツ)", 4, 16)
elif st.session_state["bubble_text"] != "":
    text_boxes = st.session_state["bubble_text"]
    st.session_state["bubble_text"] = ""
else:
    text_boxes = ""


# ---------------- fetching level data ----------------

# fetch level with certain number
df = fetch_data(st.session_state.level_data["level1"]["level_name"])
if "level" not in st.session_state:  # or st.session_state["level_change"]:
    st.session_state["level"] = df.values


# ---------------- END CONDITION ----------------
if st.session_state["player"].x == 33 and st.session_state["player"].y == 4:
    st.session_state["end"] = True

# ------------------------------------------------------------
#
#             Game enigne - frontend html renderer
#
# ------------------------------------------------------------

tab1, tab2 = st.tabs(["intro", "start game"])

# ----------------- game start --------

with tab1:
    st.subheader("| Intro")
    col1, col2 = st.columns(2, gap="small")
    with col1:
        # main_image
        st.image("graphics/other/dungeon_crawler.png")

        st.caption(
            "The Dungeon: a streamlit dungeon crawler game", unsafe_allow_html=True
        )
    with col2:
        intro_text = """
        Explore the depths of an ancient dungeon in the first streamlit-based dungeon crawler game!
        Navigate through dangerous traps, defeat fearsome monsters and uncover the secrets of the DuNgeOn.
        With intuitive controls and beautiful graphics, this game will keep you entertained for hours.
        Experience the thrill of adventure as you progress through levels and uncover powerful treasures.
        Join the adventure today and become the hero of the dungeon!
        """
        st.write(f'<p style="color:#9c9d9f">{intro_text}</p>', unsafe_allow_html=True)
        audio_file = open("audio/intro.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mpeg")

    st.subheader("| Game start")
    st.write(
        '<p style="color:#9c9d9f">To start the game go to the "start game" tab.</p>',
        unsafe_allow_html=True,
    )
    st.subheader("| Controls")
    st.write(
        '<p style="color:#9c9d9f">Desktop: please use keyboard arrows | Mobile (Android, Chrome): please use on-screen buttons | iOS: unfortunately, the auto-scrolling feature does not work yet for iOS.</p><br>',
        unsafe_allow_html=True,
    )


with tab2:

    ####################################################
    #
    #            THIS PART RENDERS MAIN SCREEN
    #
    ####################################################

    html = level_renderer(
        st.session_state["level"],
        player + enemies + boxes + voids + torches + text_boxes + chests,
    )

    display_html = st.empty()

    if st.session_state["end"] == False:
        if st.session_state["player"].alive == True:
            display_html = st.markdown(html, unsafe_allow_html=True)
        else:
            display_html = st.markdown(
                "💀 The monster was more powerful than expected, resulting in your defeat in battle. Your journey has come to an unexpected end. To continue playing, please restart the app.",
                unsafe_allow_html=True,
            )
    if st.session_state["end"] == True:
        display_html = st.markdown(
            "Thank you for playing the demo of The Dungeon. More content coming soom!",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
        <div><br>
        <a href="https://www.buymeacoffee.com/tomjohn" style="color: grey; text-decoration:none;">
        <div style="justify-content: center;margin:0px; border:solid 2px;background-color: #0e1117; ;border-radius:10px; border-color:#21212f; width: fit-content;padding:0.425rem">
        <img src="https://raw.githubusercontent.com/TomJohnH/streamlit-game/main/images/coffe.png" style="max-width:20px;margin-right:10px;">
        Buy me a coffee</a></div></div>""",
            unsafe_allow_html=True,
        )

    st.button("L", on_click=left_callback, key="L")
    st.button("R", on_click=right_callback, key="R")
    st.button("U", on_click=up_callback, key="U")
    st.button("D", on_click=down_callback, key="D")

    # ------------------------------------------------------------
    #
    #                Game enigne - sidebar for backup input
    #
    # ------------------------------------------------------------

    # ------------ sidebar for backup input ---------------------------

    with st.sidebar:
        st.write("Use keyboard arrows or buttons below")
        st.markdown("<br>", unsafe_allow_html=True)
        left_col, middle_col, right_col = st.columns([1, 1, 1])
        with middle_col:
            st.button("UP", on_click=up_callback, key="UP", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

        left_col, middle_col, right_col = st.columns([1, 1, 1])
        with left_col:
            st.button(
                "LEFT", on_click=left_callback, key="LEFT", use_container_width=True
            )

        with right_col:
            st.button(
                "RIGHT", on_click=right_callback, key="RIGHT", use_container_width=True
            )
        st.markdown("<br>", unsafe_allow_html=True)
        left_col, middle_col, right_col = st.columns([1, 1, 1])
        with middle_col:
            st.button(
                "DOWN", on_click=down_callback, key="DOWN", use_container_width=True
            )
        st.markdown("<br>", unsafe_allow_html=True)
        dev_options = st.checkbox("Developer options")

    # ------------------------------------------------------------
    #
    #               Game enigne - console div
    #
    # ------------------------------------------------------------

    st.markdown(
        f"""
        <div class="bpad" id="bpad">HP: {st.session_state["player"].hp}/20 | Gold: {st.session_state["player"].gold} | Exp: 0 </div>""",
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------
    #
    #               Game enigne - JS trickery
    #
    # ------------------------------------------------------------

    components.html(
        game_js.js_script,
        height=0,
        width=0,
    )

if dev_options:
    st.caption("Player x: " + str(st.session_state["player"].x))
    st.caption("Player y: " + str(st.session_state["player"].y))
