def sort_heuristically(t,p,d,s,debug):
    '''
    Takes arrays and sorts them large values to small.
    Returns the arrays (and d and s).
    '''
    t = sorted(t, reverse=True)
    p = sorted(p, reverse=True)
    d = d
    s = s
    if debug: print("T:{t}\nP:{p}\nD:{d}\nS:{s}\n-------------".format(t=t,p=p,d=d,s=s))
    return t,p,d,s
def populate_waitlist(t,debug):
    '''
    Takes a set of tasks and uses it to make a waitlist with those set of tasks.
    Returns waitlist.
    '''
    waitlist = []
    for task in t:
        waitlist.append(task)
        if debug: print("Adding",task,"to waitlist.\n--")
    if debug: print("----")
    return waitlist
def populate_avail_procs(p,debug):
    '''
    Takes a set of processors and uses it to make a list of those processors.
    '''
    avail = []
    for proc in p:
        avail.append(proc)
        if debug: print("Adding",proc,"to available.\n--")
    if debug: print("----")
    return avail
def check_state(st,T,P,debug):
    '''
    Returns true if state is valid.
    '''
    if len(st[1]) != len(st[2]):
        if debug: print('Count of running tasks and processors are mismatched.')
        return False
    elif len(st[0]) > len(T):
        if debug: print('Count in waitlist is more than all tasks.')
        return False 
    elif len(st[1]) + len(st[0]) + len(st[3]) != len(T):
        if debug: print('Runlist count + waitlist count + done does not equal all tasks.')
        return False
    elif len(st[2]) + len(st[4]) != len(P):
        if debug: print('Avail procs + running procs not equal.')
    else: 
        return True
def earliestFinish(st,P,debug):
    '''
    Takes a state and if it has any tasks in its runlist, find the earliest finishing task and return the index of the free processor and task. 
    If there is an empty runlist, return -1.
    '''
    finish_times = []
    processors = []
    tasks = []
    for i in range(0,len(st[2])):
        finish_time = float(st[1][i])/st[2][i]
        if debug: print("Adding",finish_time,"to finish_times.")
        finish_times.append(finish_time)
        processors.append(st[2][i])
        tasks.append(st[1][i])
    if len(finish_times) < len(P):
        if debug: print("Still need to fill up our processors.")
        return -1
    earliest = min(finish_times)
    earliestProcessor_idx = -1
    earliestTask_idx = -1
    for i in range(0,len(finish_times)):
        if finish_times[i] == earliest:
            earliestProcessor_idx = i
            earliestTask_idx = i
            break
    assert earliestProcessor_idx!=-1, "!! Problem with earliest finish."
    assert earliestTask_idx!=-1, "!! Problem with earliest finish."
    if debug: print("Returning earliest values.")
    return (earliest, earliestProcessor_idx, earliestTask_idx)
def getValue(st,debug):
    '''
    Returns the sum of done task lengths.
    '''
    total = 0
    for task in st[4]:
        total+=task
    return total
def printState(st):
    print('Waitlist:',st[0])
    print('Running tasks:',st[1])
    print('Running processors:',st[2])
    print('Completed Tasks:',st[3])
    print('Available Processors:',st[4])
    print('Start Time:',st[5])
    print('Absolute Depth:',st[6])
    print('Parent:',st[7])
    print('Children:',st[8])
    print('Unique ID:',st[9])
    