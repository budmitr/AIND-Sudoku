assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

boxes = []
row_units = []
column_units = []
square_units = []
unitlist = []
units = {}
peers = {}


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


def cross(a, b):
    """Cross product of elements in A and elements in B."""
    return [s+t for s in a for t in b]


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return dict(zip(boxes, [g if g != '.' else '123456789' for g in grid]))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    result = values.copy()

    for boxname, boxvalue in result.items():
        # Eliminate only if box has solved value
        if len(boxvalue) > 1:
            continue

        # remove solved value from all peers
        for peer in peers[boxname]:
            result[peer] = ''.join([v for v in result[peer] if v != boxvalue])

    return result


def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    result = values.copy()

    # For every unit check in which boxes does every single digit appers
    # If a digit appears only in one box, assign it as box value -- no other boxes can have this value
    for unit in unitlist:
        for digit in '123456789':
            appearence_boxes = [b for b in unit if digit in values[b]]
            if len(appearence_boxes) == 1:
                # result[appearence_boxes[0]] = digit
                assign_value(result, appearence_boxes[0], digit)

    return result


def reduce_puzzle(values):
    """
    Iterate constraint propagation (eliminate + only_choice) to reduce puzzle values

    Input: Sudoku in dictionary form
    Output: Reduced Sudoku in dictionary form OR False if stalled
    """
    result = values.copy()
    stalled = False

    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Apply constraint propagation step
        result = eliminate(result)
        # TODO: add naked_twins here
        result = only_choice(result)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return result


def search(values):
    """
    Depth-first search and constraint propagation to solve sudoku puzzle

    Input: Sudoku in dictionary form
    Output: Solved sudoku in dictionary form OR False if can't solve
    """
    # First, reduce the puzzle using the previous function
    reduced = reduce_puzzle(values)
    if reduced is False:
        return False

    # Puzzle is solved if length of values is 81, i.e. all 81 boxes have only 1 digit in it
    allvalues = ''.join(reduced.values())
    if len(allvalues) == 81:
        return reduced

    # Choose one of the unfilled squares with the fewest possibilities
    smallestbox, smallestlen = 'A1', 10
    for box in boxes:
        currentlen = len(reduced[box])
        if 1 < currentlen < smallestlen:
            smallestbox = box
            smallestlen = currentlen

    # Now use recursion to solve each one of the resulting sudokus
    # If one returns a value (not False), return that answer as a solution!
    for digit in reduced[smallestbox]:
        # Create reduced puzzle with given digit as independent search tree branch
        reduced_copy = reduced.copy()
        reduced_copy[smallestbox] = digit

        attempt = search(reduced_copy)
        if attempt is not False:
            return attempt

    # If no solution was returned, return False -- this branch has no solutions
    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    sudoku = grid_values(grid)
    solution = search(sudoku)

    return solution


if __name__ == '__main__':
    boxes = cross(rows, cols)
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # display(solve(diag_sudoku_grid))
    simple_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    display(solve(simple_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
