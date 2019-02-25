import random
import component_state as states
# "The operators on a state are either to change the assignment of one tasks, or to swap the
# assignment of two tasks."
# "For instance, one neighbor of the above state would be
# { T1 → P2, T2 → P3, T3 →P2, T4 → 0 }, changing the assignment of T2.
# Another would be { T1 → 0, T2 → 0, T3 →P2, T4 → P2 }, swapping T1 and T4."
def findQ(tasks: list, S: int, debug: bool) -> int:
    '''
    Finds the minimum Q-amount of tasks in a list before the targest value S can be reached. This resulting count is denoted by Q. 
    '''
    Qthresh = 0 # Tracking the minimum target value needed.
    Qcount = 0  # Tracking the minimum amount of tasks needed for solution (tasks sorted largest to small).
    tasks = sorted(tasks, reverse=True) # Largest to small.
    for task in tasks: 
        Qthresh += task
        Qcount += 1
        if Qthresh > S:
            break  
    return(Qcount)
def markSeen(state, seen, db):
    ''' 
    Actively marks state as seen and returns new seen list.
    '''
    stringified = str(state)
    if stringified in seen:
        seen[stringified] += 1
    else:
        seen[stringified] = 0
    return seen
def alreadySeen(state,seen,db):
    '''
    Checks if state is in seen list and returns bool.
    '''
    string = str(state)
    if string in seen:
        return seen[string]
    else:
        return 0
def changeAssignment(state,Q,conditions,seen,db):
    '''
    Finds a task and assigns a random processor (or none), returning the best neighbor of this kind.
    '''
    zero_count = 0 
    max_zero_count = len(state) - Q
    choice_count = len(conditions[1])+1
    for task_id in range(0,len(state)):
        if state[task_id+1]==0:
            zero_count += 1
    new_state_seen = 0
    task_id = 0
    best_neighbor = state.copy()
    best_score = states.loss(state,*conditions,db)
    while new_state_seen < 2 or task_id < len(state):
        curr_state = state.copy()
        if zero_count >= max_zero_count:
            assignment = random.randint(1,choice_count-1)
        else:
            assignment = random.randint(0,choice_count-1)
        if assignment == 0:
            curr_state[task_id+1] = 0
            zero_count += 1
        else:
            for i in range(1,choice_count):
                if assignment == i:
                    curr_state[task_id+1] = assignment
        assert task_id+1 in curr_state, "This state should be assigned to by now."
        if not alreadySeen(curr_state,seen,db):
            new_state_seen += 1
            seen = markSeen(curr_state,seen,db)
        else:
            task_id+=1
        score = states.loss(curr_state,*conditions,db)
        if score < best_score:
            best_neighbor = curr_state.copy()
            best_score = score 
    return best_neighbor
def swapAssignments(state,seen,conditions,db):
    '''
    Swaps a random assignment between two tasks and finds the best neighbor.
    '''
    choice_count = len(conditions[1]) + 1
    new_state_seen = 0
    task_id = 0
    best_neighbor = state
    best_score = states.loss(state,*conditions,db)
    while new_state_seen < 2 and task_id < len(state):
        curr_state = state.copy()
        assignment = random.randint(1,choice_count-1)
        for i in range(1,choice_count):
            if assignment == i:
                key = state[task_id+1]
                state[task_id+1] = state[i]
                state[i] = key
        assert task_id+1 in state and assignment in state, "These states should be assigned to by now."
        if not alreadySeen(state,seen,db):
            new_state_seen += 1
            seen = markSeen(curr_state,seen,db)
        else:
            task_id+=1
        score = states.loss(curr_state,*conditions,db)
        if score < best_score:
            best_neighbor = curr_state.copy()
            best_score = score 
    if db: print("\tClimbing to", best_neighbor)
    return best_neighbor
def climb(start_state, Q, T, P, D, S, seen, db):
    '''
    Climb to another point.
    '''
    # result = swapAssignments(start_state,seen,[T,P,D,S],db)
    result = changeAssignment(start_state,Q,[T,P,D,S],seen,db)
    return result

