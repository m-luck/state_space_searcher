import math, re, sys, anytree as tree # Import external modules.
import component_ingestInput as ingester# Import internal modules. [IO handler] 
import component_search as searcher # [search handler]
import component_stateOperators as transitioner # [handles transitioning from one state to another]
import component_stateRepresentation as states# [state handler]
def printNodeTree(start_node):  
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
            val=states.getValue(node.value, debug),
            ends=node.value[10],
            stateid=node.value[9]))
def nodify(states, childrenOf, parent_id, parent_obj):
    for child_id in childrenOf[parent_id]:
        if debug: print("Looking for state ID", child_id)
        assert states[child_id][9] == child_id, "These IDs don't match."
        new_parent_obj = tree.Node(name=child_id,value=states[child_id],parent=parent_obj)
        new_parent_id = child_id
        if child_id in childrenOf and len(childrenOf[child_id])>0:
            nodify(states, childrenOf, new_parent_id, new_parent_obj)
T = []
P = []
D = -1
S = -1
# STATE =========================================
ingester.ingest_input(sys.argv) # Processes the inputs. 
step_by_step = ingester.step_by_step
debug = ingester.debug
origT = T # Saves the original task list to be able to label T1, T2, etc., else these indices will get lost once the list is sorted. 
origP = P # Same motive as above.
T = ingester.tasks_T
P = ingester.processors_P
D = ingester.timeLimit_D
S = ingester.target_S 
T,P,D,S = states.sort_heuristically(T, P, D, S,debug) # Largest to smallest. 
# START ===============================================
task_waitlist = states.populate_waitlist(T,debug) # Tasks waiting in line to be run in any given state.
task_runlist = [] # Tasks running in any given state.
proc_runlist = [] # Processors corresponding to the indices of above running tasks.
tasks_completed = [] # Tasks already finished in any given state.
avail_procs = states.populate_avail_procs(P,debug) # Processors inactive in any state. (Will mostly be empty.)
startTime = 0
abs_depth = 0
parent = -1
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
    [*endTimes] # 10. End time of running process.
    ] # A state includes a waitlist, runlist, and a done-list. The runlist is split into tasks running with their corresponding processors.
assert states.check_state(start_state,T,P,debug) == True, "State is invalid." # Checks if the state is valid.
start_node = tree.Node(name=node_idx,value=[*start_state])
if step_by_step: print("Step #2 Starting state",start_state,"initialized.")
# OPERATE =============================================
Q, qval = searcher.findQ(T,S,debug)
Q += len(P) + Q # Due to having to fill up the processors first.
assert qval>S, "No solution." # Since findQ assumes sorted, we check that the logic does produce a qval that does surpass or match S. Else there is no answer and we return no solution. 
if step_by_step: print("Step #3 Starting depth Q ({Q}) found.".format(Q=Q))
discovered, childrenOf = searcher.iterative(start_state, D, S, Q, T, P, debug)
for parent in childrenOf:
    print(parent, childrenOf[parent])
discovered.insert(0, start_state)
for discovered_state in discovered:
    print(discovered_state[9], discovered_state)
nodify(discovered, childrenOf, 0, start_node)
printNodeTree(start_node)