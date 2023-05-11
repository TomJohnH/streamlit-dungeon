import csv
import random
import pandas as pd

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
        row_str = "".join(row)
        print(row_str[:-1])  # Removes the last character, which is the comma


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

# Convert the dungeon to a pandas DataFrame
def dungeon_to_dataframe(dungeon):
    cleaned_dungeon = []

    for row in dungeon:
        # Remove the last comma from each element
        cleaned_row = [element[:-1] for element in row]
        cleaned_dungeon.append(cleaned_row)

    return pd.DataFrame(cleaned_dungeon)

# Save the dungeon to a CSV file
def save_dungeon_to_csv(dungeon, filename="dungeon.csv"):
    with open(filename, mode="w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        for row in dungeon:
            # Remove the last comma from each element and split by comma
            cleaned_row = [element[:-1] for element in row]
            csv_writer.writerow(cleaned_row)

# Process the dungeon according to the given logic
def process_dungeon(dungeon):
    for y in range(1, HEIGHT):  # Start from 1 to avoid checking out-of-bounds index
        for x in range(WIDTH):
            if dungeon[y][x] == WALL and dungeon[y-1][x] == FLOOR:
                dungeon[y][x] = "FE3,"




# Generate and print the dungeon
dungeon = generate_dungeon()

# Process the dungeon
process_dungeon(dungeon)

print_dungeon(dungeon)

# Convert the dungeon to a pandas DataFrame
dungeon_df = dungeon_to_dataframe(dungeon)
print(dungeon_df)

save_dungeon_to_csv(dungeon)