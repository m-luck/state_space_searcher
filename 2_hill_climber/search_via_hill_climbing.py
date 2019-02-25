import math, re, sys, anytree as tree # Import external modules.
import component_ingest as ingester # Import internal modules. [IO handler] 
import component_goal as goals # [goal formatter]
import component_operators as op # [handles transitioning from one state to another]
import component_state as states# [state handler]
restart_count = 10
all_or_nothing = True # If set to true, instead of printing the closest answer found to the goal, it prints 'No solution'.
# STATE =======================================
T = []
P = []
D = -1
S = -1
ingester.ingest_input(sys.argv) # Processes the text inputs. 
# Verbosity options:
step_by_step = ingester.step_by_step # --sbs 
db = ingester.debug # --sbs --verbose
# Set to our intended values. 
T = ingester.tasks_T
P = ingester.processors_P
D = ingester.timeLimit_D
S = ingester.target_S 
conditions = [T, P, D, S] # For easy unpacking later on.
assert D != -1 and S != -1 and len(T) > 0 and len(P) > 0 
# START =======================================
empty_state = states.create_empty_state(T,db)
best_state = empty_state.copy()
best_score = S*S*D
# OPERATE =====================================
Q = op.findQ(T,S,db) # Since random start involves a chance of no processor on a task, we want to make sure we want to start in a place that can even be an answer, hence finding min-count of tasks completed, Q. 
seen = {} # Will be a record of if certain permutations have been seen. 
for i in range(0,restart_count):
    state = states.random_state(T,P,Q,db)
    while op.alreadySeen(state,seen,db) > len(T): # Start on a fresh state.
        state = states.random_state(T,P,Q,db)
    score = states.loss(state,*conditions,db)
    if db:
        print("New starting state",i+1,"is",state)
        print("\t==Loss is", states.loss(state,*conditions,db))
    if score < best_score:
        if step_by_step: print("Found a new best state!", state, "with score",score)
        best_state = state.copy() 
        if db: print('Setting best state to', best_state)
        best_score = score
    seen = op.markSeen(state, seen, db)
    climb_done = False
    new_state = state.copy()
    while climb_done == False:
        new_state = op.climb(new_state, Q, *conditions, seen, db).copy() # Climb to a new state.
        score =  states.loss(new_state,*conditions,db)
        if db:
            print("\t==Loss of current is", score)
        if op.alreadySeen(new_state,seen,db) > len(T):
            climb_done = True 
        else:
            seen = op.markSeen(new_state, seen, db)
        if score < best_score:
            if step_by_step: print("Found a new best state!", new_state, "with score",score)
            best_state = new_state.copy()
            if db: print('Setting best state to', best_state)
            best_score = score
        if db:
            print("\t\tBest is", best_score)
# GOAL =============================================
# Given the nature of randomness and chosen loss heuristic, the correct answer will come a proportion of the time, hopefully at least more than 50%. 
if step_by_step: print(best_state)
res = []
ind = 0
for processor in best_state: # Create X X X X...
    if ind < len(empty_state):
        ind += 1
        res.append(str(best_state[processor]))
res = ' '.join(res)
# Since it returns the closest thing it found to an answer, we can always have it print a state.
# If we wanted to check if it's actually an answer, can check if it's a goal. 
if goals.isGoal(best_state, *conditions, db) or all_or_nothing is False:
    print(res)
else: 
    print("No solution.")






