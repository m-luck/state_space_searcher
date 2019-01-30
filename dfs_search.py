
class State:
    def __init__(self,index=-1,parent=None,successors=[]):
        self.parent = parent
        self.successors = successors
        self.index = index
        child_ind = -1
    def getNextChild(self):
        self.child_ind += 1
        return self.child_ind
    def getParent(self):
        return self.parent
    def getIndex(self):
        return self.index
    def setIndex(indexself):
        self.index = index
    def setParent(parentself):
        self.parent = parent
    def succeed(childself):
        successors.append(child)
    def details(self):
        return "ID: "+str(self.getIndex())+"| Parent: "+str(self.getParent())
node = State(0)

print(node.details())
