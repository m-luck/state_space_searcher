from state_in_tree import State
from anytree import Node, RenderTree


# class State:
#     def __init__(self,index=-1,parent=None,successors=[]):
#         self.parent = parent
#         self.successors = successors
#         self.index = index
#         child_ind = -1
#     def getNextChild(self):
#         self.child_ind += 1
#         return self.child_ind
#     def getParent(self):
#         return self.parent
#     def getIndex(self):
#         return self.index
#     def setIndex(indexself):
#         self.index = index
#     def setParent(parentself):
#         self.parent = parent
#     def succeed(childself):
#         successors.append(child)
#     def details(self):
#         return "ID: "+str(self.getIndex())+"| Parent: "+str(self.getParent())

tasks = [12,42,48,54]
processors = [2,3]
parent = None
nodes = []
nodes.append()



for pre, fill, node in RenderTree(nodes[1]):
    print("%s%s" % (pre, node.name))
