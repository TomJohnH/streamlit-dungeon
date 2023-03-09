import game_config
import game_js
import game_def
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


# ------------------------------------------------------------
#
#                        Callbacks
#
# ------------------------------------------------------------


def left_callback():

    if game_def.character_can_move(
        st.session_state[
            "level"
        ],  # note the different order of x and y. Done to confuse myself in the future.
        # good luck future me
        game_config.tileset_movable,
        st.session_state["player"].y,
        st.session_state["player"].x - 1,
    ):
        st.session_state["player"].x -= 1
        st.session_state.left_clicked = True
        st.session_state["steps"] += 1

    # REFACTOR THIS!

    # this little loop is responsible for moving the monsters and reacting to encounters
    for i in range(0, len(st.session_state["monsters"])):
        # game_def.random_move(st.session_state["monsters"][i])
        game_def.move_to_player(
            st.session_state["player"], st.session_state["monsters"][i]
        )
        game_def.encounter(st.session_state["player"], st.session_state["monsters"][i])
    for i in range(0, len(st.session_state["chests"])):
        game_def.treasures(st.session_state["player"], st.session_state["chests"][i])


def right_callback():
    # player movement
    if game_def.character_can_move(
        st.session_state["level"],
        game_config.tileset_movable,
        st.session_state["player"].y,
        st.session_state["player"].x + 1,
    ):
        st.session_state["player"].x += 1
        st.session_state.right_clicked = True
        st.session_state["steps"] += 1

    for i in range(0, len(st.session_state["monsters"])):
        # game_def.random_move(st.session_state["monsters"][i])
        game_def.move_to_player(
            st.session_state["player"], st.session_state["monsters"][i]
        )
        game_def.encounter(st.session_state["player"], st.session_state["monsters"][i])
    for i in range(0, len(st.session_state["chests"])):
        game_def.treasures(st.session_state["player"], st.session_state["chests"][i])


def up_callback():
    if game_def.character_can_move(
        st.session_state["level"],
        game_config.tileset_movable,
        st.session_state["player"].y - 1,
        st.session_state["player"].x,
    ):
        st.session_state["player"].y -= 1
        st.session_state.up_clicked = True
        st.session_state["steps"] += 1

    for i in range(0, len(st.session_state["monsters"])):
        # game_def.random_move(st.session_state["monsters"][i])
        game_def.move_to_player(
            st.session_state["player"], st.session_state["monsters"][i]
        )
        game_def.encounter(st.session_state["player"], st.session_state["monsters"][i])
    for i in range(0, len(st.session_state["chests"])):
        game_def.treasures(st.session_state["player"], st.session_state["chests"][i])


def down_callback():
    if game_def.character_can_move(
        st.session_state["level"],
        game_config.tileset_movable,
        st.session_state["player"].y + 1,
        st.session_state["player"].x,
    ):
        st.session_state["player"].y += 1
        st.session_state.down_clicked = True
        st.session_state["steps"] += 1

    for i in range(0, len(st.session_state["monsters"])):
        # game_def.random_move(st.session_state["monsters"][i])
        game_def.move_to_player(
            st.session_state["player"], st.session_state["monsters"][i]
        )
        game_def.encounter(st.session_state["player"], st.session_state["monsters"][i])
    for i in range(0, len(st.session_state["chests"])):
        game_def.treasures(st.session_state["player"], st.session_state["chests"][i])


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


# ------------------------------------------------------------
#
#                        Graphics engine
#
# ------------------------------------------------------------

# ---------------- CSS ----------------

local_css("style.css")


# ------------------------------------------------------------
#
#             Game enigne - frontend html creator
#
# ------------------------------------------------------------

# --------------- level config ------------------------


current_level_name = "level1"

if "level_data" not in st.session_state:
    level_config = game_config.level_config
    st.session_state.level_data = json.loads(level_config)


# ---------------- INTERACTIVE LEVEL ELEMENTS ----------------

# ---------------- creating player html ----------------

if "player" not in st.session_state:
    temp = st.session_state.level_data["players_stats"]
    temp_xy = st.session_state.level_data[current_level_name]["player_xy"]
    st.session_state["player"] = Character(
        x=temp_xy["x"],
        y=temp_xy["y"],
        file=temp["file"],
        hp=temp["hp"],
        gold=temp["gold"],
        alive=temp["alive"],
    )

player = f"""
<img src="{game_config.player_img}" id="player" class="player" style="grid-column-start: {st.session_state["player"].x}; grid-row-start: {st.session_state["player"].y};">"""

# ---------------- creating monsters html ----------------

# we are constructing monsters in iteractions based on level configuration
if "monsters" not in st.session_state:
    st.session_state["monsters"] = []

    for monsters_name in st.session_state.level_data[current_level_name]["monsters"]:
        temp = st.session_state.level_data[current_level_name]["monsters"][
            monsters_name
        ]
        st.session_state["monsters"].append(
            Character(
                x=temp["x"],
                y=temp["y"],
                file=temp["file"],
                hp=temp["hp"],
                gold=temp["gold"],
                alive=temp["alive"],
            )
        )

# we are creating monsters html


monsters = game_def.monsters_html(st.session_state["monsters"])


# ---------------- chests ----------------

# chests are interactive therfore we are creating objects

if "chests" not in st.session_state:
    st.session_state["chests"] = []

    for chests_name in st.session_state.level_data[current_level_name]["chests"]:
        temp = st.session_state.level_data[current_level_name]["chests"][chests_name]
        st.session_state["chests"].append(
            InanimateObject(
                x=temp["x"],
                y=temp["y"],
                file=temp["file"],
                visible=temp["visible"],
            )
        )

chests = game_def.chests_html(st.session_state["chests"])

# ---------------- NON-INTERACTIVE LEVEL ELEMENTS ----------------

# ---------------- boxes ----------------

if "boxes" not in st.session_state:
    st.session_state["boxes"] = game_def.additional_layers_html(
        current_level_name, "boxes"
    )

boxes = st.session_state["boxes"]

# ---------------- voids ----------------

if "voids" not in st.session_state:
    st.session_state["voids"] = game_def.additional_layers_html(
        current_level_name, "voids", "xyz"
    )

voids = st.session_state["voids"]

# ---------------- troches ----------------

if "torches" not in st.session_state:
    st.session_state["torches"] = game_def.additional_layers_html(
        current_level_name, "torches"
    )

torches = st.session_state["torches"]

# ---------------- creating visual layers textboxes ----------------


text_boxes_html = game_def.text_boxes(
    st.session_state["player"].x, st.session_state["player"].y, current_level_name
)


# ------------------------------------------------------------
#
#             fetching level data from csv
#
# ------------------------------------------------------------

# fetch level with certain number
df = fetch_data(st.session_state.level_data[current_level_name]["level_csv"])
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
        '<p style="color:#9c9d9f">To start the game go to the "start game" tab. Please be sure to switch to <b>dark mode</b> or the custom theme. The Dungeon is meant to be played in the dark! </p>',
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

    html = game_def.level_renderer(
        st.session_state["level"],
        player + monsters + boxes + voids + torches + text_boxes_html + chests,
    )

    display_html = st.empty()

    if st.session_state["end"] == False:
        if st.session_state["player"].alive == True:
            display_html = st.markdown(html, unsafe_allow_html=True)
        else:
            display_html = st.markdown(
                "💀 The monster was more powerful than expected, resulting in your defeat in battle. Your journey has come to an unexpected end. To continue playing, please restart the app.<br><br>",
                unsafe_allow_html=True,
            )
            if st.button("restart"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.experimental_rerun()
                st.experimental_rerun()
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
    st.caption(
        game_def.distance_from_player(
            st.session_state.player, st.session_state["monsters"][0]
        )
    )
    st.caption(
        game_def.move_to_player(
            st.session_state.player, st.session_state["monsters"][0]
        )
    )
