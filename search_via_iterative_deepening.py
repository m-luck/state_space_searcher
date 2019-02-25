import math, re, sys, anytree as tree # Import external modules.
import component_ingestInput as ingester# Import internal modules. [IO handler] 
import component_search as searcher # [search handler]
import component_stateOperators as transitioner # [handles transitioning from one state to another]
import component_stateRepresentation as states# [state handler]

# Visual Display==========================================================================================
# =========Run with 'python search_via_iterative_deepening [file] --sbs --verbose' to activate ===========
def printNodeTree(start_node, t_speeds, debug):
    '''
    Print out a right angle tree of the generated state space.
    '''
    for pre, fill, node in tree.RenderTree(start_node):
        print("{pre}ID:{id} Parent:{stateparent} Depth: {depth} Time: {start}\n\
        {pre} RunningT: {task_run}\n\
        {pre} RunningP: {proc_run}\n\
        {pre} End time: {ends}\n\
        {pre} Waitlist: {waitlist}\n\
        {pre} Procs Avail: {proc_avail}\n\
        {pre} Tasks Done: {task_done}\n\
        {pre} Value: {val}\n".format(pre=pre, id=node.name, parent=node.parent, 
            waitlist=node.value[0],
            task_run=node.value[1],
            proc_run=node.value[2],
            task_done=node.value[3],
            proc_avail=node.value[4],
            start=node.value[5],
            depth=node.value[6],
            stateparent=node.value[7],
            val=states.getValue(node.value, t_speeds, debug),
            ends=node.value[10],
            stateid=node.value[9]))
def nodify(states, childrenOf, parent_id, parent_obj):
    '''
    Create a tree of the generated state space.
    '''
    for child_id in childrenOf[parent_id]:
        if debug: print("Looking for state ID", child_id)
        assert states[child_id][9] == child_id, "These IDs don't match."
        new_parent_obj = tree.Node(name=child_id,value=states[child_id],parent=parent_obj)
        new_parent_id = child_id
        if child_id in childrenOf and len(childrenOf[child_id])>0:
            nodify(states, childrenOf, new_parent_id, new_parent_obj)

# STATE =========================================
T = []
P = []
D = -1
S = -1
ingester.ingest_input(sys.argv) # Processes the inputs. 
step_by_step = ingester.step_by_step # Step by step == true will print a concise log of what the program is doing. 
debug = ingester.debug # Debug == true will print out a detailed log of what the program is doing.
T = ingester.tasks_T
P = ingester.processors_P
D = ingester.timeLimit_D
S = ingester.target_S 
origT = [*T] # Saves the original task list to be able to label T1, T2, etc., else these indices will get lost once the list is sorted. 
origP = [*P] # Same motive as above.
# Further deconstruct the tasks/processors into their value dictionaries and their labels (T1, T2, etc).
T_lengths = {}
P_speeds = {}
# While not in the example, this program acknowledges that some situations may have tasks of equal length and processors of equal speed. To make sense, each needs to be tracked via index.
T_inds = []
P_inds = []
# Moreover, since we will sort the tasks and processors, we also need to keep a relationship between sorted and unsorted.
T_sortedToNot = {}
P_sortedToNot = {}
T,P,D,S = states.sort_heuristically(T, P, D, S,debug) # Largest to smallest. 
for proc in range(0, len(P)):
    P_speeds[proc+1] = P[proc]
    for origProcSpeedInd in range(0,len(origP)):
        if origP[origProcSpeedInd] == P_speeds[proc+1]:
            P_sortedToNot[proc+1] = origProcSpeedInd+1
    P_inds.append(proc+1)
for task in range(0, len(T)):
    T_lengths[task+1] = T[task]
    for origTaskLengthInd in range(0,len(origT)):
        if origT[origTaskLengthInd] == T_lengths[task+1]:
            T_sortedToNot[task+1] = origTaskLengthInd+1
    T_inds.append(task+1)

# START ============================================
task_waitlist = states.populate_waitlist(T_inds,debug) # Tasks waiting in line to be run in any given state.
task_runlist = [] # Tasks running in any given state.
proc_runlist = [] # Processors corresponding to the indices of above running tasks.
tasks_completed = [] # Tasks already finished in any given state.
avail_procs = states.populate_avail_procs(P_inds,debug) # Processors inactive in any state. (Will mostly be empty.)
startTime = 0
abs_depth = 0
parent = -1 # No parent to begin.
children = []
node_idx = 0 # Will iterate for IDs on new tree nodes. 
endTimes = []
start_state = [
    [*task_waitlist],#0
    [*task_runlist],#1
    [*proc_runlist],#2
    [*tasks_completed],#3
    [*avail_procs],#4
    startTime, #5
    abs_depth, #6
    parent, #7
    [*children], #8 
    node_idx, #9
    [*endTimes] # 10. 
    ] # A state includes a waitlist, runlist, and a done-list. The runlist is split into tasks running with their corresponding processors, and absolute end times.
assert states.check_state(start_state,T,P,debug) == True, "State is invalid." # Checks if the state is valid.
start_node = tree.Node(name=node_idx,value=[*start_state])
if step_by_step: print("Step #2 Starting state",start_state,"initialized.")

# OPERATE =============================================
Q, qval = searcher.findQ(T,S,debug) # Find our Q, the reasonable starting value to even have hope of an answer.
Q += len(P) # Due to having to fill up the processors first, which takes initial depth of len(P) depth for loop invariance.
assert qval>S, "No solution." # Since findQ assumes sorted, we check that the logic does produce a qval that does surpass or match S. Else there is no answer and we return no solution. 
if step_by_step: print("Step #3 Starting depth Q ({QP}, really {Q}) found.".format(Q=Q, QP=Q-len(P)))
goal = -1 # Goal will change from -1 if found.
if step_by_step: print("Step #4 Iterative deepening of operator has begun!")
assert goal == -1, "Goal must be -1 (not found) to start."
while goal == -1:
    if step_by_step: print("Attempting iterative deeping with effective depth",str(Q-len(P))+". --")
    discovered, childrenOf, goal = searcher.iterative(start_state, D, S, Q, T_inds, P_inds, T_lengths, P_speeds, debug)
    for parent in childrenOf:
        if debug: print(parent, childrenOf[parent])
    discovered.insert(0, start_state) # Did not originally include root, so we include it.
    for discovered_state in discovered:
        if debug: print(discovered_state[9], discovered_state)
    nodify(discovered, childrenOf, 0, start_node) # For use in display mode. 
    if debug: printNodeTree(start_node,T_lengths,debug)
    if step_by_step and goal == -1: print("\tDid not find goal at this depth.")
    Q+=1 # Iterate max depth, per iterative deepening.

# GOAL ==================================================
if goal != -1:
    if step_by_step: print("\tFound goal!")
    if debug: states.printState(discovered[goal],T_lengths,debug)
    leafToRootPath = [] # Will trace the nodes in the successful path.
    child_id = goal
    while child_id != 0: # Trace this path.
        leafToRootPath.append(child_id)
        child_id =  discovered[child_id][7]
    pairings = {} # The eventual answer set of {Tn:Pn...}
    leafToRootPath.reverse()  # Sort from root to leaf.
    if debug: print(leafToRootPath)
    for state_id in leafToRootPath: # Create the pairings, running them through the dictionaries we created at the start.
        tasks_running = discovered[state_id][1]
        processors = discovered[state_id][2]
        for i in range(0,len(tasks_running)):
            pairings[T_sortedToNot[tasks_running[i]]]=P_sortedToNot[processors[i]]
    answer_id = leafToRootPath[-1] 
    tasks_unfinished = discovered[answer_id][1] # The tasks still running in the goal state.
    for task in tasks_unfinished: # We want to make them assigned to no processor since they do not need to be run.
        pairings[T_sortedToNot[task]] = 0 # This task is not pertinent, so assign it to processor "0", i.e. none.
    answer_string = []
    for i in range(0,len(T)):
        answer_string.append(str(pairings[i+1])) # Format it as 'X X X X...', i.e. processor ID per each task
    answer_string =' '.join(answer_string)
    print(answer_string)

else: 
    print("No solution.") # No solution otherwise. 