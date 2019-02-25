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
def isGoal(target_state: list, D, S, t_lengths, debug):
    '''
    Returns if the state matches the goal.
    '''
    if target_state[5]<D and states.getValue(target_state, t_lengths, debug) >= S:
        if debug: print("I found a goal state!")
        return (True, target_state[9])
    else:
        return (False, -1)
def timeUp(time, D, debug):
    '''
    Returns if time limit is reached.
    '''
    res = False
    if  (time >= D):
        if debug: print('Times up!',time,"passed",D)
        res = True
    return res
def maxDepthReached(depth,max_depth, debug):
    '''
    Returns if a given depth has reached a given max depth.
    '''
    res = False
    if (depth >= max_depth):
        if debug: print('Max depth reached!',depth,"passed",max_depth)
        res = True
    return res
def emptyRunList(target_state, debug):
    '''
    Returns true is runlist has length 0.
    '''
    res = False
    if len(target_state[1])==0:
        if debug: print('Empty runlist!')
        res = True
    return res
def emptyWaitList(target_state, debug):
    '''
    Returns true is waitlist has length 0.
    '''
    res = False
    if len(target_state[0])==0:
        if debug: print('Empty waitlist!')
        res = True
    return res
def shouldGenerate(target_state, D, S, max_depth, t_lengths, debug):
    '''
    Decides to generate children, i.e. if given state is not an ultimate or depth-wise leaf or goal. Also notifies if state is a goal.
    '''
    time = target_state[5]
    depth = target_state[6]
    found, goal = isGoal(target_state, D, S, t_lengths, debug)
    if found:
        return (False, goal)
    if timeUp(time, D, debug) or maxDepthReached(depth, max_depth, debug) or (emptyRunList(target_state, debug) and emptyWaitList(target_state, debug)):
        return (False, -1)
    else:
        return (True, -1)
def generateChildren(generateList: list, max_depth, D, S, T, P, startInd, t_lengths, p_speeds, debug):
    '''
    Generates a set of children given a list of parents. Also notifies if a goal state is found within.
    '''
    states_generated = []
    goalFound = -1
    while len(generateList)>0:
        target_state = generateList[0]
        assert states.check_state(target_state,T,P,debug)==True, "This state is not valid: "+str(target_state)
        del generateList[0]
        go, anyGoal = shouldGenerate(target_state, D, S, max_depth, t_lengths, debug)
        if (go):
            if states.earliestFinish(target_state, P, debug) == -1:
                time = target_state[5]
                freeProc = -1
                freeTask = -1
            else:
                time, freeProc, freeTask = states.earliestFinish(target_state,P, debug)
            new_states, startInd = ops.updateState(target_state,time,freeProc,freeTask,target_state[9],startInd,t_lengths, p_speeds,debug)
            for new_state in new_states:
                generateList.insert(0, new_state)
                states_generated.append(new_state)
        else:
            if debug: print("Not generating........")
            if anyGoal != -1:
                goalFound = anyGoal
    return states_generated, goalFound
             
def iterative(root, D, S, Q, T, P, t_lengths, p_speeds, debug):
    '''
    Builds one iteration of the search, storing the tree.
    '''
    generateList = [root]
    if debug: print('Discovering children...')
    full_tree, anyGoal = generateChildren(generateList, Q, D, S, T, P, 0, t_lengths, p_speeds, debug)
    childrenOf = {}
    for state in full_tree:
        if state[7] in childrenOf: # If the parent is already in the dictionary...
            childrenOf[state[7]].append(state[9]) # ...Add this node to its children list. 
        else: 
            childrenOf[state[7]] = [] # Else do the same thing but first initialize the array. 
            childrenOf[state[7]].append(state[9]) # Add this node to its children list. 
    return full_tree, childrenOf, anyGoal
