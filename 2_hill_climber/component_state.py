import random
# "A state is a complete assignment to each task of either a processor number or 0, meaning not
# on the schedule. For example { T1 → P2, T2 → 0, T3 →P2, T4 → 0 }"
def create_empty_state(T,db):
    state = {}
    for i in range(0,len(T)):
        state[i+1] = 0
    return state
def random_state(T,P,Q,db):
    '''
    Generates a random state.
    '''
    state = {}
    max_zero_count = len(T) - Q 
    zero_count = 0
    choice_count = len(P)+1 # Each task has a 1-in-len(P) chance of being assigned a certain processor. If we include the lack of a processor, we +1 to the denominator. 
    for task_id in range(0,len(T)):
        if zero_count >= max_zero_count:
            assignment = random.randint(1,choice_count-1)
        else:
            assignment = random.randint(0,choice_count-1)
        if assignment == 0:
            state[task_id+1] = 0
            zero_count += 1
        else:
            for i in range(1,choice_count):
                if assignment == i:
                    state[task_id+1] = assignment
        assert task_id+1 in state, "This state should be assigned to by now." 
    return state
def loss(state, T, P, D, S, db):
    '''
    "The cost function is (the shortfall on the value) + (the overflow on the time)." 
    We have weighted these with heuristics below.
    '''
    if db: print("------")
    value = 0
    elapsed = {}
    for processor_id in range(0,len(P)):
        elapsed[processor_id+1] = 0
    for task_id in range(0,len(T)):
        processor_id = state[task_id+1]-1
        if state[task_id+1] == 0:
            value += 0
        else:
            runtime = T[task_id] / float(P[processor_id]) # Length divided by assigned speed.   
            elapsed[processor_id+1] += runtime # Keep track of elapsed time per processor.
            value += float(T[task_id])
    latest_finish = 0
    for processor in elapsed:
        finish = elapsed[processor]
        if finish > latest_finish:
            latest_finish = finish # This is the longest elapsed time of all the processors, hence our bottleneck.
    shortfall = S - value
    overflow = latest_finish - D
    if overflow < 0: # Respect winners.
        if shortfall <= 0:
            shortfall *= int(shortfall*S)*int(-overflow*D) # Weighted in proportion to target value and time limit. An answer will be supremely good.
            overflow *= int(shortfall*S)*int(-overflow*D)
    else:
        overflow *= int(D*overflow) # Weighted in proportion to time limit. High penalty.
        if shortfall > 0:
            shortfall *= shortfall
    # We will keep at these general heuristics, else we might overfit. 

    if db: print("\tValue Shortfall:",shortfall,"| Time Overflow:",overflow)
    return shortfall+overflow
