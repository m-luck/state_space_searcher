from anytree import Node, RenderTree
# Author: Michael Lukiman. After reading Chang et al. (1994)
tasks = [12,42,48,54]
processors = [2,3]
# A. START state
queue = [] # Elements in format (int taskName, int executionTime)
ind = 0 # Generic index for program
for task in tasks: # All tasks are ready to run
    queue.append((ind,task))
    ind += 1
queue = sorted(queue, key=lambda task: task[1], reverse = True ) # Sort waitlist by executionTime
running = [] # Elements in format (int taskName, int assignedProcessor, int stopTime)
completion = 0 # Elements in format int finishingTime
node = [queue,[*running], completion] # Contains all of the above in a data structure
root = Node(0,None,value=node) # will contain all nodes
tree = [root] # Save tree as a list for simplicity
processors = sorted(processors, reverse=True)
# That concludes the initialization.
# B. SUCCESSOR states (Operator logic)
ind = 0
node_ind = 1
parent = root
# print(queue)
for pro in processors:
    # print(pro)
    task = (queue[ind][0])
    runtime = (queue[ind][1])
    running.append((task,pro,runtime/float(pro)+completion))
    queue = queue[:ind]+queue[ind+1:]
    ind += 1
# print(running)
bottleneck = min(running, key=lambda task: task[2])[2]
new_node = [queue,running,bottleneck]
new_node = Node(node_ind,parent,value=new_node)
for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.value))
