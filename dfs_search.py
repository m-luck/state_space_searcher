from anytree import Node, RenderTree
# Author: Michael Lukiman. After reading Chang et al. (1994)
D = 33 # Goal to complete all tasks by time D
# =========== A. STATE representation
waitlist = [] # Tasks needed to be run e.g. [{ 'task': 0, 'computeCost': 12}, { 'task': 1, 'computeCost': 42}] OR just [*task compute times] depending on how human friendly we want the output.
running = [] # Tasks in the process of running e.g. [{'task': 2, 'onProcessor': 0, 'speed': 2, 'computeTimeRemaining': 21, 'startTime':0, 'finishTime':18}, {'task': 3, 'onProcessor': 1, 'speed': 3, 'computeTimeRemaining': 18, 'startTime':0, 'finishTime':18}]. The more info the easier the debugging.
earliestFinishTime = 0 # AKA d_min = min(running, key=lambda task: task['computeTimeRemaining'])['computeTimeRemaining']
finalFinishTime = 0 # AKA d_max = max(...)
startTime = 0
time = 0
state = {'waitlist':[*waitlist],'runlist':[*running],'start':startTime,'earliestFinish':earliestFinishTime,'latestFinish':finalFinishTime} # Clear and effective to be nodes in a tree. Not designed to be memory lean. Uses unpacking to make sure each state does not refer to the same frozen list.
# =========== B. START state
processors = [2,3]
tasks = [12,42,48,54]
ind=0
for task in tasks:
    waitlist.append({'index':ind, 'computeTime':task})
    ind += 1
root = Node(name=0,value=state)
# That concludes the initialization.
# =========== C. SUCCESSOR states (Operator logic)
# Update the state with the next possible state
# next = Node(node_ind,parent,value=new_node)
def generateChildren():
    for state in RenderTree(root):
        state = state.value
        stateTransition = state['earliestFinish']
        if len(running) > 1:
            freeProcessor = min(running, key=lambda x: x['finishTime'])
        for task in state['waitlist']:
            state['waitlist'].remove(task)
            state['runlist'].append({'task':task['index'], 'onProcessor':freeProcessor['onProcessor'], 'speed':freeProcessor['speed'], 'computeTimeRemaining':task['computeTime'], 'startTime':time, })

# =========== D. GOAL
# State with empty waitlist, empty runlist, and completion time < D
# Display tree.
for pre, fill, node in RenderTree(root):
    print("{0}NODE {1}\n{0}Waitlist: {2}\n{0}Runlist: {3}\n{0}Start: {4}\n{0}Earliest: {5}\n{0}Latest: {6}".format(pre, node.name, node.value['waitlist'], node.value['runlist'], node.value['start'], node.value['earliestFinish'], node.value['latestFinish'], ))
