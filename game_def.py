import game_config
import streamlit as st
from random import randrange

# ---------------- check surroundings ----------------

# this function checks if move is "legal"


def character_can_move(level_matrix, tileset_movable, x, y):
    if tileset_movable[level_matrix[x - 1, y - 1]] == True:
        return True
    else:
        pass


def random_move(movable_object):

    # this function is responsible for random movement of monsters
    # it will be changed in the future - monsters will follow the player
    # is it possible? yes. check https://rogue-rpg.streamlit.app/

    rnd_move = randrange(100)
    # st.write("random_move" + str(rnd_move))
    if rnd_move < 25:
        if character_can_move(
            st.session_state["level"],
            game_config.tileset_movable,
            movable_object.y,
            movable_object.x + 1,
        ):
            movable_object.x += 1
    if rnd_move >= 25 and rnd_move < 50:
        if character_can_move(
            st.session_state["level"],
            game_config.tileset_movable,
            movable_object.y,
            movable_object.x - 1,
        ):
            movable_object.x -= 1
    if rnd_move >= 50 and rnd_move < 75:
        if character_can_move(
            st.session_state["level"],
            game_config.tileset_movable,
            movable_object.y + 1,
            movable_object.x,
        ):
            movable_object.y += 1
    if rnd_move >= 75 and rnd_move < 100:
        if character_can_move(
            st.session_state["level"],
            game_config.tileset_movable,
            movable_object.y - 1,
            movable_object.x,
        ):
            movable_object.y -= 1
