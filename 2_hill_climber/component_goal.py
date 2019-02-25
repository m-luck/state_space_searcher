def isGoal(state, T, P, D, S, db):
    '''
    Returns true if is valid answer state.
    '''
    res = False
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
            return True
    return res