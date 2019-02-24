import component_stateRepresentation as states
def updateState(st,earlTime,earlProc_idx,earlTask_idx,parent,startInd, debug)->list:
    # Should be 7 updates, one for each list + one time + one depth in a state.
    # 1. Waitlist update
    children = []
    for i in range(0,len(st[0])):
        startInd+=1
        waitlist=[*st[0]]
        task_run=[*st[1]]
        proc_run=[*st[2]]
        done=[*st[3]]
        avail=[*st[4]]
        time=st[5]
        abs_depth=st[6]
        up_next = waitlist[i]
        waitlist.remove(waitlist[i])
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
        if debug: print("Removing", avail[0])
        del avail[0]
        # 6. Update time.
        # 7. Update depth.
        # 8. Parent.
        if debug: 
            print("New start time is",earlTime)
            print("Parent is", parent)
        state = [[*waitlist],[*task_run],[*proc_run],[*done],[*avail], earlTime, abs_depth+1, parent, [], startInd] # The spanking new state! It's deterministic!
        children.append(state)
    return children, startInd