import math, re, sys, anytree as tree # Import external modules.
import component_ingest as ingester # Import internal modules. [IO handler] 
import component_goal as goals # [goal formatter]
import component_operators as op # [handles transitioning from one state to another]
import component_state as states# [state handler]
restart_count = 10
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
best_score = states.loss(best_state,*conditions,db)
if db: print("Start state:",empty_state) 
# OPERATE =====================================
Q = op.findQ(T,S,db) # Since random start involves a random chance of no processor on a task, we want to make sure we want to start in a place that can even be an answer, hence finding min-count of tasks completed, Q. 
seen = {} # Will be a record of if certain permutations have been seen. 
for i in range(0,restart_count):
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
        new_state = op.climb(new_state, Q, *conditions, seen, db) 
        score =  states.loss(new_state,*conditions,db)
        if db:
            print("\t==Loss of current is", score)
        if op.alreadySeen(new_state,seen,db):
            climb_done = True
        if score < best_score:
            if step_by_step: print("Found a new best state!", new_state, "with score",score)
            best_state = new_state.copy()
            if db: print('Setting best state to', best_state)
            best_score = score
        if db:
            print("\t\tBest is", best_score)
if step_by_step: print(best_state)
res = []
ind = 0
for processor in best_state:
    if ind < len(empty_state):
        ind += 1
        res.append(str(best_state[processor]))
res = ' '.join(res)
print(res)





