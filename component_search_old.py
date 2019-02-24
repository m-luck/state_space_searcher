from anytree import Node, RenderTree
def search(depth, method, root, searchInd, previousNode, Ds, S, children):
    traversed = []
    stack = [root]
    found = False
    answer = None
    while stack and found == False:
        cur_node = stack[0]
        traversedNode = Node(name = searchInd, value=cur_node, parent=previousNode)
        searchInd += 1
        previousNode = traversedNode
        stack = stack[1:]
        traversed.append(cur_node)
        # print(cur_node)
        if cur_node in children:
            if method == 'DFS':
                for child in children[cur_node]:
                    stack.insert(0, child)
            elif method == 'BFS':
                for child in children[cur_node]:
                    stack.append(child)
        done = 'False'
        if len(cur_node.value['waitlist']) == 0:
            done = 'True'
        # print("Latest Finish",cur_node.value['latestFinish'],"| Done:", done, "| Final Value:", cur_node.value['value'])
        # if done == 'True' and cur_node.value['latestFinish'] < D and timeOrTarget == 0:
            # found = True
            # answer=cur_node
        # elif cur_node.value['latestFinish'] < Ds and cur_node.value['value'] > S and timeOrTarget == 1:
        if cur_node.value['latestFinish'] < Ds and cur_node.value['value'] > S:
            found = True
            answer=cur_node
    count = 0
    for node in traversed:
        # print(node.name)
        count += 1
    # print("Total traversed:", count)
    # print("Path:")
    # cur_node = answer
    # print(cur_node,"\n")
    # while cur_node.parent:
        # print(cur_node.parent,"\n")
        # cur_node = cur_node.parent
    return traversed
def DFS(depth, root, searchInd, previousNode, Ds, S, children):
    return search(depth, 'DFS', root, searchInd, previousNode, Ds,S, children)
def BFS(depth, root, searchInd, previousNode, Ds, S, children):
    return search(depth, 'BFS', root, searchInd, previousNode, Ds, S, children)