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
best_state = empty_state
if db: print("Start state:",empty_state) 
# OPERATE =====================================
Q = op.findQ(T,S,db) # Since random start involves a random chance of no processor on a task, we want to make sure we want to start in a place that can even be an answer, hence finding min-count of tasks completed, Q. 
for i in range(0,restart_count):
    state = states.random_state(T,P,Q,db)
    seen = {} # Will be a record of if certain permutations have been seen. 
    seen = states.markSeen(state, T, seen, db)
    if db:
        print("New starting state",i+1,"is",state)
        print("\t==Score is", states.score(state,*conditions,db))
    op.climb(random_state, Q, *conditions, seen, db) 





# "The cost function is (the shortfall on the value) + (the overflow on the time).""