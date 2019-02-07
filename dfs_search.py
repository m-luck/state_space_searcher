from anytree import Node, RenderTree
# Author: Michael Lukiman. After reading Chang et al. (1994)
D = 33 # Goal to complete all tasks by time D
# =========== A. STATE representation
waitlist = [] # Tasks needed to be run e.g. [{ 'task': 0, 'computeCost': 12}, { 'task': 1, 'computeCost': 42}] OR just [*task compute times] depending on how human friendly we want the output.
running = [] # Tasks in the process of running e.g. [{'task': 2, 'onProcessor': 0, 'speed': 2, 'computeTimeRemaining': 21, 'startTime':0, 'finishTime':18}, {'task': 3, 'onProcessor': 1, 'speed': 3, 'computeTimeRemaining': 18, 'startTime':0, 'finishTime':18}]. The more info the easier the debugging.
earliestFinishTime = 0 # AKA d_min = min(running, key=lambda task: task['computeTimeRemaining'])['computeTimeRemaining']
finalFinishTime = 0 # AKA d_max = max(...same as above...)
startTime = 0
currentTime = 0
state = {'waitlist':[*waitlist],'runlist':[*running],'start':startTime,'earliestFinish':earliestFinishTime,'latestFinish':finalFinishTime} # Clear and effective to be nodes in a tree. Uses unpacking to make sure each state does not refer to the same frozen list.
# =========== B. START state
processors = [2,3] # speed
tasks = [12,42,48,54] # compute time required
ind=1 # Since we will define empty root as ind=0 manually
for task in tasks:
    waitlist.append({'index':ind, 'computeTime':task})
    ind += 1
root = Node(name=0,value=state)
# That concludes the initialization.
# =========== C. SUCCESSOR states (Operator logic)
# Update the state with the next possible state, through a queue of children
generateList = [root] # This will be in the form of queue, removing the first element at a time
# next = Node(node_ind,parent,value=new_node)
def generateChildren():
    for state in generateList:
        parent = state # will be added as parent to all children nodes
        generateList.remove(state) # will remove the state from the generate queue before we change its variable
        state_id = state.name # keep track of the index
        state = state.value # 'state' from now on refers to the state's value
        stateTransitionTime = state['earliestFinish'] # this is the time from which the new state will start
        if len(running) > 1:
            freeProcessorTask = min(running, key=lambda x: x['finishTime']) # This is the task with the finished processor (the earliest finishTime). If there are more than one with the same finish time, it is no problem, the next state will permute on the next one (with the same starting time).
            state['runlist'].remove(freeProcessorTask) # Since it is finished, the updated state will not have the task in the runlist
            target_processor = freeProcessorTask['onProcessor'] # This will be referenced when loading a new task on this processor
            currentTime = freeProcessorTask['finishTime'] # the current time in the simulation is the time our task just finished. This will be used as the start time of a new task.
        else: # But if there's no tasks in the runlist at all
            target_processor = processors[0] # If there's no runlist to pull from, just take the first processor in the list
            processors.remove(target_processor, 1) # We want to cycle the processor so the next processor is up in the queue and...
            processors.append(target_processor) # ...the current processor is added to the end of the queue
        for task in state['waitlist']: # We want to permute assigning one waiting task from the waitlist to this processor
            ind += 1 # Iterate the index so each node has a unique index
            state['waitlist'].remove(task) # Since it is about to be assigned to the runlist, it is no longer on the waitlist
            state['waitlist'] = [*state['waitlist']] # unpacked
            state['runlist'].append({'task':task['index'], 'onProcessor':target_processor, 'speed':freeProcessorTask['speed'], 'computeTimeRemaining':task['computeTime'], 'startTime': currentTime, 'finishTime':task['computeTime']/float(freeProcessorTask['speed']) }) # It is now in the runlist
            state['runlist'] = [*state['runlist']] # unpacked
            # To be readable, the new state is:
            # 'task': task['index']
            # 'onProcessor': target_processor (defined above)
            # 'speed': freeProcessorTask['speed']
            # 'computeTimeRemaining': task['computeTime']
            # 'startTime': currentTime
            # 'finishTime': task['computeerTime']/float(freeProcessorTask['speed'])
            new_node = Node(name=ind, value=state, parent=parent) # The new node has name: unique ind, value: whole state above, parent: the node we're permuting on
            generateList.append(new_node) # Adding this to the generateList, because we will eventually find the children of this node (breadth-first)
    if len(generateList) > 0:
        generateChildren()
generateChildren(root)

# =========== D. GOAL
# State with empty waitlist, empty runlist, and completion time < D
# Display tree.
for pre, fill, node in RenderTree(root):
    print("{0}NODE {1}\n{0}Waitlist: {2}\n{0}Runlist: {3}\n{0}Start: {4}\n{0}Earliest: {5}\n{0}Latest: {6}".format(pre, node.name, node.value['waitlist'], node.value['runlist'], node.value['start'], node.value['earliestFinish'], node.value['latestFinish'], ))
