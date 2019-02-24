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
    if target_state['time']<D and target_height['value'] >= S:
        return True
    else:
        return False
def timeUp(time, D, debug):
    return (time >= D)
def maxDepthReached(depth,max_depth, debug):
    return (depth >= max_depth)
def emptyRunList(target_state, debug):
    return len(target_state[1])==0
def shouldGenerate(target_state, D, S, max_depth, debug):
    time = target_state[5]
    depth = target_state[6]
    if isGoal(target_state, D, S, debug) or timeUp(time, D, debug) or maxDepthReached(depth, max_depth, debug) or emptyRunList(target_state, debug):
        return False
    else:
        return True
def generateChildren(generateList: list, max_depth, D, S, startInd, debug):
     states_generated = []
     while len(generateList)>0:
        target_state = generateList[0]
        assert states.check_state(target_state,T,P,debug)==True, "This state is not valid: "+str(target_state)
        del generateList[0]
        if shouldGenerate(target_state, D, S, max_depth, debug):
            startInd += 1
            time, freeProc, freeTask = states.earliestFinish(target_state)
            new_state = ops.updateState(target_state,time,freeProc,freeTask,target_state,startInd,debug)
            target_state[7].append(startInd) 
            generateList.insert(0, new_state)
            if debug: 
                print("Discovering state:")
                printState(new_state)
             
def iterative(root, D, S, Q, debug):
    '''
    '''
    generateList = [root]
    generateChildren(generateList, Q, D, S, 0, debug)