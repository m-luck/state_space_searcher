from tree_maker import *
def sort_heuristically(t, p, D, s):
    global tasks, processors, Ds, S
    '''
    Takes arrays and sorts them large values to small
    '''
    tasks = sorted(t, reverse=True)
    processors = sorted(p, reverse=True)
    Ds = D
    S = s
    
    