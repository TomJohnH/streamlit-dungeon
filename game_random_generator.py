import random

# Constants
FLOOR = "FP,"
WALL = "E,"
WIDTH = 50
HEIGHT = 50

# Initialize the dungeon with walls
def initialize_dungeon():
    return [[WALL for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Check if the given coordinates are within the dungeon bounds
def in_bounds(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

# Randomly walk through the dungeon, carving out floors
def random_walk(dungeon, start_x, start_y, num_steps):
    x, y = start_x, start_y
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for _ in range(num_steps):
        dx, dy = random.choice(directions)
        nx, ny = x + dx, y + dy

        if in_bounds(nx, ny):
            dungeon[ny][nx] = FLOOR
            x, y = nx, ny

# Print the dungeon in a human-readable format
def print_dungeon(dungeon):
    for row in dungeon:
        print("".join(row))

# Generate a dungeon using the Random Walk algorithm
def generate_dungeon():
    dungeon = initialize_dungeon()

    # Start the random walk in the center of the dungeon
    start_x, start_y = WIDTH // 2, HEIGHT // 2
    dungeon[start_y][start_x] = FLOOR

    # Carve out floors using random walk
    num_steps = 1000
    random_walk(dungeon, start_x, start_y, num_steps)

    return dungeon

# Generate and print the dungeon
dungeon = generate_dungeon()
print_dungeon(dungeon)