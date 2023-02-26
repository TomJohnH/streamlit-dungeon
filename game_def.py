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


# ---------------- visual gimmicks ----------------


def text_bubble_html(text, x, y):
    return f"""<div class="container_text" style="position: relative; grid-column-start: {x}; grid-row-start: {y}; grid-column-end: {x+4};"><img src="https://raw.githubusercontent.com/TomJohnH/streamlit-dungeon/main/graphics/other/message.png"><div style="position: absolute; top: 40%;left: 50%;transform: translate(-50%, -50%);font-size:0.875rem;">{text}</div></div>"""
