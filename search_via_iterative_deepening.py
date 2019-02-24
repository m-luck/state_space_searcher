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
        {pre} Waitlist: {waitlist}\n\
        {pre} Procs Avail: {proc_avail}\n\
        {pre} Tasks Done: {task_done}\n\
        {pre} Children: {children}\n".format(pre=pre, id=node.name, parent=node.parent, 
            waitlist=node.value[0],
            task_run=node.value[1],
            proc_run=node.value[2],
            task_done=node.value[3],
            proc_avail=node.value[4],
            start=node.value[5],
            depth=node.value[6],
            stateparent=node.value[7],
            children=node.value[8],
            stateid=node.value[9]))
def nodify(nodes, children, ind, parent):
    for child in children[ind]:
        prnt = tree.Node(name=nodes[child][9],value=nodes[child],parent=parent)
        if child in children:
            if len(children[child])>0:
                nodify(nodes, children, nodes[child][9], prnt)
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
    node_idx #9
    ] # A state includes a waitlist, runlist, and a done-list. The runlist is split into tasks running with their corresponding processors.
assert states.check_state(start_state,T,P,debug) == True, "State is invalid." # Checks if the state is valid.
start_node = tree.Node(name=node_idx,value=[*start_state])
if step_by_step: print("Step #2 Starting state",start_state,"initialized.")
# OPERATE =============================================
Q, qval = searcher.findQ(T,S,debug)
Q += len(P) + 1 # Due to having to fill up the processors first.
assert qval>S, "No solution." # Since findQ assumes sorted, we check that the logic does produce a qval that does surpass or match S. Else there is no answer and we return no solution. 
if step_by_step: print("Step #3 Starting depth Q ({Q}) found.".format(Q=Q))
discovered, nope = searcher.iterative(start_state, D, S, Q, T, P, debug)
discovered_dict = {}
parent = start_node
children = {}
for state in discovered:
    discovered_dict[state[9]] = state
    print(state[9],state)
    if state[7] in children:
        children[state[7]].append(state[9])
    else: 
        children[state[7]] = []
        children[state[7]].append(state[9])
for child in children:
    print(child, children[child])
for child in children:
    nodify(discovered_dict,children,child,parent)
printNodeTree(start_node)