
class State:
    def __init__(self,value=None,index=-1,parent=-1,successors=[]):
        self.parent = parent
        self.successors = successors
        self.index = index
        self.value = None
        child_ind = -1
    def getValue(self):
        return self.value
    def getNextChild(self):
        self.child_ind += 1
        return self.child_ind
    def getParent(self):
        return self.parent
    def getIndex(self):
        return self.index
    def setIndex(self, index):
        self.index = index
    def setParent(self, parent):
        self.parent = parent
    def succeed(self, child):
        successors.append(child)
    def setValue(self, value):
        self.value = value
    def details(self):
        return "ID: "+str(self.getIndex())+"| Parent: "+str(self.getParent())
node = State(0)
print(node.details())
