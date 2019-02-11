from anytree import Node, RenderTree
# Author: Michael Lukiman. After reading Chang et al. (1994)
includeRedundantPermutations = False
includeEmptyProcessorBranch = True
D = 33 # Goal to complete all tasks by time D
# =========== A. STATE representation
waitlist = [] # Tasks needed to be run e.g. [{ 'task': 0, 'computeCost': 12}, { 'task': 1, 'computeCost': 42}] OR just [*task compute times] depending on how human friendly we want the output.
running = [] # Tasks in the process of running e.g. [{'task': 2, 'onProcessor': 0, 'speed': 2, 'computeTimeRemaining': 21, 'startTime':0, 'finishTime':18}, {'task': 3, 'onProcessor': 1, 'speed': 3, 'computeTimeRemaining': 18, 'startTime':0, 'finishTime':18}]. The more info the easier the debugging.
earliestFinishTime = 0 # AKA d_min = min(running, key=lambda task: task['computeTimeRemaining'])['computeTimeRemaining']
finalFinishTime = 0 # AKA d_max = max(...same as above...)
startTime = 0
currentTime = 0
# =========== B. START state
processors = [2,3] # speed
tasks = [12,42,48,54] # compute time required
ind = 1
taskInd = 0 # to enumerate task IDs at init
seenPermutations = {}
for task in tasks:
    waitlist.append({'index':taskInd, 'computeTime':task})
    taskInd += 1
state = {'waitlist':waitlist,'runlist':running,'start':startTime,'earliestFinish':earliestFinishTime,'latestFinish':finalFinishTime} # Clear and effective to be nodes in a tree. Uses unpacking to make sure each state does not refer to the same frozen list.
root = Node(name=0,value=state)
# That concludes the initialization.
# =========== C. SUCCESSOR states (Operator logic)
# Update the state with the next possible state, through a queue of children
generateList = [root] # This will be in the form of queue, removing the first element at a time
# next = Node(node_ind,parent,value=new_node)
def generateChildren():
    global ind
    global waitlist
    global running
    global processors
    global tasks
    global generateList
    for state in generateList:
        parent = state # will be added as parent to all children nodes
        generateList.remove(state) # will remove the state from the generate queue before we change its binding
        state_id = state.name # keep track of the index
        state = state.value # 'state' from now on refers to the state's value
        freeProcessorTask = None
        if len(state['runlist']) == len(processors) or len(state['waitlist']) == 0: # if the processors are running at full capacity or the waitlist is done
            freeProcessorTask = min(state['runlist'], key=lambda x: x['finishTime']) # This is the task with the finished processor (the earliest finishTime). If there are more than one with the same finish time, it is no problem, the next state will permute on the next one (with the same starting time).
            target_processor = freeProcessorTask['onProcessor'] # This will be referenced when loading a new task on this processor
            currentTime = state['earliestFinish']# the current time in the simulation is the time our task just finished. This will be used as the start time of a new task.
        else: # But if there's no tasks in the runlist at all, or is not yet full capacity
            target_processor = processors[0] # If there's no runlist to pull from, just take the first processor in the list
            processors.remove(target_processor) # We want to cycle the processor so the next processor is up in the queue and...
            processors.append(target_processor) # ...the current processor is added to the end of the queue
            currentTime = 0
        if includeEmptyProcessorBranch == True:
            state['waitlist'].append('deactivated')
        for task in state['waitlist']: # We want to permute assigning one waiting task from the waitlist to this processor
            save_waitlist = [*state['waitlist']] # make a new list with identical elements, so they are independent
            save_waitlist.remove(task) # Since it is about to be assigned to the runlist, it is no longer on the waitlist
            save_runlist = [*state['runlist']]
            if len(state['runlist']) == len(processors):# if the processors are running at full capacity
                save_runlist.remove(freeProcessorTask) # we established that this is the candidate that finished, so it is no longer running. we will use the processor to run this next task.
            if task == 'deactivated':
                save_runlist.append({\
                    'task':-1,\
                    'onProcessor':target_processor,\
                    'speed':target_processor,\
                    'computeTimeRemaining':,\
                    'startTime': currentTime,\
                    'finishTime':task['computeTime']/float(target_processor)\
                    }) # The task is now in the runlist            else:
                freeProcessorTask = min(state['runlist'], key=lambda x: x['finishTime'])
                save_runlist.append({\
                    'task':task['index'],\
                    'onProcessor':target_processor,\
                    'speed':target_processor,\
                    'computeTimeRemaining':task['computeTime'],\
                    'startTime': currentTime,\
                    'finishTime':task['computeTime']/float(target_processor)\
                    }) # The task is now in the runlist
                earliestFinishTime = min(save_runlist, key=lambda x: x['finishTime'])['finishTime']
                finalFinishTime = max(save_runlist, key=lambda x: x['finishTime'])['finishTime']
                save_state = { 'waitlist':save_waitlist,'runlist':save_runlist,'start':currentTime,'earliestFinish':earliestFinishTime,'latestFinish':finalFinishTime }
                if includeRedundantPermutations == True:
                    permutation_full = sorted(save_runlist, key=lambda x: x['task'])
                    permutation_tasks = []
                    for item in permutation_full:
                        item = (item['task'],item['onProcessor'])
                        permutation_tasks.append(item)
                    permutation_tasks.append(save_waitlist)
                    permutation_tasks = str(permutation_tasks)
                    print(permutation_tasks)
                    if permutation_tasks not in seenPermutations:
                        ind += 1 # Iterate the index so each node has a unique index
                        new_node = Node(name=ind, value=save_state, parent=parent) # The new node has name: unique ind, value: whole state above, parent: the node we're permuting on
                        generateList.append(new_node) # Adding this to the generateList, because we will eventually find the children of this node (breadth-first)
                        seenPermutations[permutation_tasks] = True
                    else:
                        print("seen")
                else:
                    ind += 1 # Iterate the index so each node has a unique index
                    new_node = Node(name=ind, value=save_state, parent=parent) # The new node has name: unique ind, value: whole state above, parent: the node we're permuting on
                    generateList.append(new_node) # Adding this to the generateList, because we will eventually find the children of this node (breadth-first)
    if len(generateList) > 0: # while there are states to generate, recursively generate them
        generateChildren()
generateChildren()

# =========== D. GOAL
# State with empty waitlist, empty runlist, and completion time < D
# Display tree.
for pre, fill, node in RenderTree(root):
    print("{0}NODE {1}\n{0}Waitlist: {2}\n{0}Runlist: {3}\n{0}Start: {4}\n{0}Earliest: {5}\n{0}Latest: {6}".format(pre, node.name, node.value['waitlist'], node.value['runlist'], node.value['start'], node.value['earliestFinish'], node.value['latestFinish'], ))
