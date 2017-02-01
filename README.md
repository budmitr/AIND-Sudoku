# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Within a given unit I define which values are naked twins -- they are equal, 2 symbls long and appear only twice.
Having these defined, I eliminated possible values from other boxes in current unit.
I used python's `set` to simplify elimination since digits can have unordered positions.
Full code of naked_twins presented below

```
result = values.copy()

# Find all instances of naked twins
for unit in unitlist:
    # First, collect values of current unit
    vals = [values[box] for box in unit]

    # Iterate over values and select only values with length of 2 which occure 2 times
    twins = set([v for v in vals if len(v) == 2 and vals.count(v) == 2])

    # If no twins found, make next iteration
    if not len(twins):
        continue

    # Eliminate!
    for box in unit:
        # Eliminate only from values with length bigger than 2
        if len(result[box]) < 3:
            continue

        # Represent box value as set to use subset operation
        boxset = set(result[box])
        for t in twins:
            # if set(t).issubset(boxset):
            boxset = boxset - set(t)

        result[box] = ''.join(sorted(list(boxset)))

return result
```

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Constraint propagation already includes a set of row, column and 3x3 units.
I just added 2 diagonal units into list and used them within already prepared flow of elimination and only-choice methods.
Here is a snipped of generating 2 additional diag units:
```
diag_units = [
    [rows[i] + cols[i] for i in range(9)],
    [rows[::-1][i] + cols[i] for i in range(9)],
]
```

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.