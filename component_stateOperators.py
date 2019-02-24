import component_stateRepresentation as states
def updateState(st,earlTime,earlProc_idx,earlTask_idx,parent,startInd, debug)->list:
    # Should be 7 updates, one for each list + one time + one depth in a state.
    waitlist=st[0]
    task_run=st[1]
    proc_run=st[2]
    done=st[3]
    avail=st[4]
    time=st[5]
    abs_depth=st[6]
    up_next = -1
    # 1. Waitlist update
    if len(waitlist)!=0:
        up_next = waitlist[0] # First element of waitlist is up next.
        del waitlist[0] # Removes first element from waitlist.
    if debug: print("Readied next task from waitlist.")
    # 5. Done task update.
    if earlProc_idx != -1 and earlTask_idx != -1:
        done.append(task_run[earlTask_idx])
        avail.append(proc_run[earlProc_idx])
        del task_run[earlTask_idx]
        del proc_run[earlProc_idx]
        if debug: print("Removed free processor and task from running, labeled to available and done respectively.")
    # 2. Run task update.
    task_run.append(up_next)
    if debug: print("Added task length",up_next,"to running.")
    assert len(avail)>0, "There should be an available processor because we just freed one."
    # 3. Run processor update.
    proc_run.append(avail[0])
    if debug: print("Assigned proc speed",avail[0],"to that task.")
    # 4. Available processor update.
    del avail[0]
    # 6. Update time.
    # 7. Update depth.
    # 8. Parent.
    if debug: print("New start time is",earlTime)
    state = [[*waitlist],[*task_run],[*proc_run],[*done],[*avail], earlTime, abs_depth+1, parent, [], startInd] # The spanking new state! It's deterministic!
    return state