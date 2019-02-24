import component_stateOperators as ops
import component_stateRepresentation as states
def findQ(tasks: list, S: int, debug: bool) -> int:
    '''
    Finds the minimum first Q-amount of tasks in an ordered task list before the targest value S can be reached. This result count is denoted by Q.
    Assumes tasks are sorted large to small. 
    '''
    Qthresh = 0 # Tracking the minimum target value needed.
    Qcount = 0  # Tracking the minimum amount of tasks needed for solution (tasks sorted largest to small).
    for task in tasks: 
        if debug: print("Task:",task)
        Qthresh += task
        Qcount += 1
        if debug:
            print("Qthresh now:",Qthresh)
            print("Qcount now:",Qcount,"\n----")
        if Qthresh > S:
            if debug: print("Found",Qthresh,"bigger than S",S,"\n----------------")
            break  
    return(Qcount, Qthresh)
def isGoal(target_state: list, D, S, debug):
    if target_state[5]<D and states.getValue(target_state, debug) >= S:
        if debug: print("I found a goal state!")
        return True
    else:
        return False
def timeUp(time, D, debug):
    res = False
    if  (time >= D):
        if debug: print('Times up!',time,"passed",D)
        res = True
    return res
def maxDepthReached(depth,max_depth, debug):
    res = False
    if (depth >= max_depth):
        if debug: print('Max depth reached!',depth,"passed",max_depth)
        res = True
    return res
def emptyRunList(target_state, debug):
    res = False
    if len(target_state[1])==0:
        if debug: print('Empty runlist!')
        res = True
    return res
def emptyWaitList(target_state, debug):
    res = False
    if len(target_state[0])==0:
        if debug: print('Empty waitlist!')
        res = True
    return res
def shouldGenerate(target_state, D, S, max_depth, debug):
    time = target_state[5]
    depth = target_state[6]
    if isGoal(target_state, D, S, debug) or timeUp(time, D, debug) or maxDepthReached(depth, max_depth, debug) or (emptyRunList(target_state, debug) and emptyWaitList(target_state, debug)):
        return False
    else:
        return True
def generateChildren(generateList: list, max_depth, D, S, T, P, startInd, debug):
    states_generated = []
    while len(generateList)>0:
        target_state = generateList[0]
        assert states.check_state(target_state,T,P,debug)==True, "This state is not valid: "+str(target_state)
        del generateList[0]
        if shouldGenerate(target_state, D, S, max_depth, debug):
            if states.earliestFinish(target_state, P, debug) == -1:
                time = target_state[5]
                freeProc = -1
                freeTask = -1
            else:
                time, freeProc, freeTask = states.earliestFinish(target_state,P, debug)
            new_states, startInd = ops.updateState(target_state,time,freeProc,freeTask,target_state[9],startInd,debug)
            for new_state in new_states:
                generateList.insert(0, new_state)
                states_generated.append(new_state)
        else:
            if debug: print("Not generating........")
    return states_generated
             
def iterative(root, D, S, Q, T, P, debug):
    '''
    '''
    generateList = [root]
    if debug: print('Discovering children...')
    full_tree = generateChildren(generateList, Q, D, S, T, P, 0, debug)
    childrenOf = {}
    for state in full_tree:
        if state[7] in childrenOf: # If the parent is already in the dictionary...
            childrenOf[state[7]].append(state[9]) # ...Add this node to its children list. 
        else: 
            childrenOf[state[7]] = [] # Else do the same thing but first initialize the array. 
            childrenOf[state[7]].append(state[9]) # Add this node to its children list. 
    return full_tree, childrenOf
