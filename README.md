Welcome to mll469's state space searcher project for Ernest Davis' Artificial Intelligence graduate course.

Thank you for taking time to read. 

## There are three folders, two of which should be relevant:
* 1_iterative_deepener: This is the iterative deepening source code.
* 2_hill_climber: This is the hill climbing source code. 

# Setting up the environment:
The code is written in Python 3.
All source code is united under one intended virtual environment already prepared. If pipenv is not yet installed on the user, run
    
    python3 -m pip install --user pipenv

The environment should be installed with

    python3 -m pipenv install 

and started with 

    python3 -m pipenv shell

(https://pipenv.readthedocs.io/en/latest/)
Courant machines are compatible and have been tested with the source code. 
However, in the lack of pipenv compatibility, the packages intended to be installed are listed in the file 'Pipfile'.

Each command has an optional step-by-step rundown, appending 
 
    --sbs 
(step-by-step) as an option after the file input.
For a very detailed and verbose rundown, append 

    --sbs --verbose

# To run iterative deepener:
    cd 1_iterative_deepener
    python3 search_via_iterative_deepening [formatted_file] (--sbs --verbose)

# To run hill climber:
    cd 2_hill_climber
    python3 search_via_hill_climbing [formatted_file] (--sbs --verbse)

By default, these will both print the intended processor assignment in order of tasks in the file, or 'No solution.' if a goal was not found while running. 

###### If something doesn't work, simply email mll469@nyu.edu.
###### Thank you! Michael Lukiman, February 2019

The directory 0_homework_draft is a running draft from the previous homework, included to show progress.
