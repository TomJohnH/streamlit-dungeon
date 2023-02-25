# ---------------- check surroundings ----------------

# this function checks all potential moves


def character_can_move(logic_layer, tileset_movable, x, y):
    if tileset_movable[logic_layer[x - 1, y - 1]] == True:
        return True
    else:
        pass
