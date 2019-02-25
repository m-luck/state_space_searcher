Welcome to mll469's state space searcher project for Ernest Davis' Artificial Intelligence graduate course.

Thank you for taking time to read. 

## There are three folders, two of which should be relevant:
    * 1_iterative_deepener: This is the iterative deepening source code.
    * 2_hill_climber: This is the hill climbing source code. 

# Setting up the environment:
The code is written in Python 3.
All source code is united under one intended virtual environment already prepared. The environment should be installed with 
>pipenv install 
and started with 
>pipenv shell
Courant machines are compatible with these virtual environments. 
However, in the lack of pipenv compatibility, the packages intended to be installed are listed in the file 'Pipfile'.

Each command has an optional step-by-step rundown, appending 
    --sbs 
(step-by-step) as an option after the file input.
For a very detailed and verbose rundown, append 
    --sbs --verbose

# To run iterative deepener:
    cd 1_iterative_deepener
    python search_via_iterative_deepening [formatted_file] (--sbs --verbose)

# To run hill climber:
    cd 2_hill_climber
    python search_via_hill_climbing [formatted_file] (--sbs --verbse)

By default, these will both print the intended processor assignment in order of tasks in the file, or 'No solution.' if a goal was not found while running. 

###### If something doesn't work, simply email mll469@nyu.edu.
###### Thank you! Michael Lukiman