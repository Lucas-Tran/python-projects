def blank_map(width, height):
    return [[None for _ in range(height)] for _ in range(width)]

def random_map(width, height, random):
    return [[((random.randint(0, 10), random.randint(0, 21))) for _ in range(height)] for _ in range(width)]

def default_map(width, height, row, column):
    grid = blank_map(width, height)
    
    grid[0][0] = (row + 2, column)
    grid[0][1] = (row + 1, column)
    grid[0][2] = (row, column)

    grid[width - 1][0] = (row + 2, column + 2)
    grid[width - 1][1] = (row + 1, column + 2)
    grid[width - 1][2] = (row, column + 2)

    for x in range(1, width - 1):
        grid[x][0] = (row + 2, column + 1)

    for x in range(1, width - 1):
        grid[x][1] = (row + 1, column + 1)

    for x in range(1, width - 1):
        grid[x][2] = (row, column + 1)
    return grid