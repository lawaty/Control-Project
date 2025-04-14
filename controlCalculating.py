import numpy as np
import sympy as sp

#input :
#    graph

#output:
#       {
#       "result":                                    the transferFunction (string),
#       "compinationsOfUntouchedLoops":              the compination of loops (2d array index i is all compinations of (i+1)loops),
#       "delta":                                     the delta, 
#       "delta From 1 to M":                         deltas from 1 to m
#       }


def normalize_cycle(nodes, weights):
    nodes = nodes[:-1]
    n = len(nodes)
    min_index = min(range(n), key=lambda i: nodes[i])


    rotated_nodes = nodes[min_index:] + nodes[:min_index]
    rotated_weights = weights[min_index:] + weights[:min_index]

    rotated_nodes.append(rotated_nodes[0])

    return tuple(rotated_nodes), tuple(rotated_weights)

def remove_duplicate_cycles(cycles_list):
    seen = set()
    unique = []

    for path, weights in cycles_list:
        norm_nodes, norm_weights = normalize_cycle(path, weights)
        if (norm_nodes, norm_weights) not in seen:
            seen.add((norm_nodes, norm_weights))
            unique.append((list(norm_nodes), list(norm_weights)))

    return unique

def dfs_forward_paths(cur_node, graph, visited, cur_path, paths, cur_weight):
    if visited[cur_node] == 1 or (len(cur_path) > 0 and cur_path[-1] > cur_node):
        return

    visited[cur_node] = 1
    cur_path.append(cur_node)

    if cur_node == len(graph) - 1:
        paths.append((cur_path.copy(), cur_weight.copy()))
    else:
        for node, weight in graph[cur_node]:
            cur_weight.append(weight)
            dfs_forward_paths(node, graph, visited, cur_path, paths, cur_weight)
            cur_weight.pop()

    cur_path.pop()
    visited[cur_node] = 0

def forward_paths(graph):
    visited = [0 for _ in range(len(graph))]
    cur_path = []
    cur_weight = []
    paths = []
    dfs_forward_paths(0, graph, visited, cur_path, paths, cur_weight)
    return paths

def dfs_cycles(cur_node, graph, visited, cur_path, cycles, cur_weight):
    if visited[cur_node] == 1:
        if cur_path[-1] < cur_node:
            return
        idx = cur_path.index(cur_node)
        cur_path.append(cur_node)
        cycles.append((cur_path[idx:].copy(), cur_weight[idx:].copy()))
        cur_path.pop()
        return

    visited[cur_node] = 1
    cur_path.append(cur_node)

    for node, weight in graph[cur_node]:
        cur_weight.append(weight)
        dfs_cycles(node, graph, visited, cur_path, cycles, cur_weight)
        cur_weight.pop()

    cur_path.pop()
    visited[cur_node] = 0

def cycles(graph):
    visited = [0 for _ in range(len(graph))]
    cur_path = []
    cur_weight = []
    cycles = []
    dfs_cycles(0, graph, visited, cur_path, cycles, cur_weight)
    return remove_duplicate_cycles(cycles)


def compile(input,n):
    array2d=[]
    weights=[]
    for tuple in input:
        array=[]
        for j in range(n):
            array.append(0)
        for index in tuple[0]:
            array[index] =1
        array2d.append(array)
        newWeight=sp.Float(1.0)
        for weight in tuple[1]:
            try:
                num=float(weight)
                weight=sp.Float(num)
            except (ValueError, TypeError) as e:
                
                weight=sp.simplify(weight)
            newWeight *=weight
        weights.append(newWeight)
    return (array2d,weights)


#input :
#       numOfNodes (number of nodes in the graph)
#       numOfLoops (number of loops in the graph)
#       numOfPaths (number of forword paths in the graph)
#       arrayOfLoops (array of the values of every loop (can be sympols or numerical))
#       arrayOfPaths (same as before but for paths)
#       nodesInLoops (it is 2d array every loop has an array has all the nodes that loop if nodesInLoops[i]=1 then node[i] is in the loop 
#        if  nodesInLoops[i]=0 then node[i] is not in the loop)
#       nodesInPaths (same as before but in the paths)
#

def UnTouchedLoops(numOfNodes, numOfLoops, arrayOfLoops, nodesInLoops):
    nonTouchedLoops=[]
    for i in range(numOfLoops):
        nonTouchedLoops.append(f"L{i+1}")
        try:
            num=float(arrayOfLoops[i])
            arrayOfLoops[i]=sp.Float(num)
        except (ValueError, TypeError) as e:
            
            arrayOfLoops[i]=sp.simplify(arrayOfLoops[i])
            
    numOfUntouched=np.ones(numOfLoops)
    for i in range(numOfLoops):
        for j in range(i + 1, numOfLoops):
            x = np.zeros(numOfNodes)
            for k in range(numOfNodes):
                x[k] = nodesInLoops[i][k] + nodesInLoops[j][k]
                if x[k] > 1:
                    break
                if k == numOfNodes - 1:  # Only append if we finish the loop without breaking
                    nodesInLoops = np.vstack([nodesInLoops, x])
                    arrayOfLoops=np.append(arrayOfLoops,arrayOfLoops[i] * arrayOfLoops[j])
                    numOfUntouched = np.append(numOfUntouched,numOfUntouched[i]+numOfUntouched[j])
                    nonTouchedLoops.append(f"{nonTouchedLoops[j]} {nonTouchedLoops[i]}")
    n1=numOfLoops
    n2=len(arrayOfLoops)
    while(not n1==n2 ):
        for i in range(numOfLoops):
            for j in range(n1,n2):
                        x = np.zeros(numOfNodes)
                        for k in range(numOfNodes):
                            x[k] = nodesInLoops[i][k] + nodesInLoops[j][k]
                            if x[k] > 1:
                                break
                            if k == numOfNodes - 1:  # Only append if we finish the loop without breaking
                                if not any((x == row).all() for row in nodesInLoops):
                                    nodesInLoops = np.vstack([nodesInLoops, x])
                                    arrayOfLoops=np.append(arrayOfLoops,arrayOfLoops[i] * arrayOfLoops[j])
                                    numOfUntouched = np.append(numOfUntouched,numOfUntouched[i]+numOfUntouched[j])
        n1=n2
        n2=len(arrayOfLoops)                           
    compNonToucheddLoops=[]
    for i in range(int(max(numOfUntouched))):
        compNonToucheddLoops.append([])

    for i in range(len(nonTouchedLoops)):
        compNonToucheddLoops[int(numOfUntouched[i])-1].append(nonTouchedLoops[i])

    return arrayOfLoops,numOfUntouched,compNonToucheddLoops

def untouchedLoopWithPath(numOfNodes, numOfLoops,arrayOfLoops,nodesInLoops,nodesInPath):
    newArrayOfLoops = np.array([])
    newNodesInLoops = newNodesInLoops = np.empty((0, numOfNodes))
    for i in range(numOfLoops):
        for j in range(numOfNodes):
            if nodesInLoops[i][j] and nodesInPath[j]==1:
                break
            if j==numOfNodes-1:
                newArrayOfLoops=np.append(newArrayOfLoops,arrayOfLoops[i])
                newNodesInLoops=np.vstack([newNodesInLoops,nodesInLoops[i]])            
    return newArrayOfLoops,newNodesInLoops     

def getDelta(arrayOfLoops,numOfUntouched):
    
    result = sp.Integer(1)
    for i in range (len(arrayOfLoops)):
        try:
            result += (-1)**(numOfUntouched[i])*sp.Float(arrayOfLoops[i])
        except:
            result += (-1)**(numOfUntouched[i])*arrayOfLoops[i]
    return result

def deltaFrom1ToM(numOfNodes, numOfLoops,numOfPaths, arrayOfLoops, nodesInLoops,nodesInPaths):
    deltas = np.empty(numOfPaths)
    i=0
    for path in nodesInPaths:
        l1,l2=untouchedLoopWithPath(numOfNodes, numOfLoops,arrayOfLoops,nodesInLoops,path)
        if len(l1) ==0:
            deltas[i]=sp.Integer(1)
        else:
            l3,l4,_=UnTouchedLoops(numOfNodes, len(l1),l1,l2)
            deltas[i]=getDelta(l3,l4)
        i +=1
    return deltas  

def getTransferFunction(numOfNodes, numOfLoops,numOfPaths, arrayOfLoops,arrayOfPaths, nodesInLoops,nodesInPaths):
    deltas=deltaFrom1ToM(numOfNodes, numOfLoops,numOfPaths, arrayOfLoops, nodesInLoops,nodesInPaths)
    l1,l2,compNonToucheddLoops=UnTouchedLoops(numOfNodes, numOfLoops, arrayOfLoops, nodesInLoops)
    delta=getDelta(l1,l2)
    result=sp.Integer(0)
    i=0
    for path in arrayOfPaths:
        path=sp.simplify(path)
        try:
            path=sp.simplify(path)
        except (ValueError, TypeError) as e:
            num=float(path)
            path=sp.Float(num)
        result += path*deltas[i]
        i +=1
    result =(result/delta)
    for i in range(len(deltas)):
        deltas[i]=str(deltas[i])
    delta =str(delta) 
    return{
        "result":str(result),
        "compinationsOfUntouchedLoops":compNonToucheddLoops,
        "delta":delta,
        "delta From 1 to M":deltas     
    }
 
def pipLine(graph):
    n=len(graph)
    paths=forward_paths(graph)
    loops=cycles(graph)
    nodesInLoops,arrayOfLoops=compile(loops,n)
    nodesInPaths,arrayOfPaths=compile(paths,n)
    return getTransferFunction(n, len(arrayOfLoops),len(arrayOfPaths), arrayOfLoops,arrayOfPaths, nodesInLoops,nodesInPaths)






# Test data
#a = np.array([[0,0,1,1,0], [0,1,1,1,0]])
#b = ["-g2*h1", "-g1*g2*h2"]
#Ps=np.array([[1,1,1,1,1],[1,0,1,1,1]])
#arrayOfPaths = ["g1*g2","g2"]
# Call the function
#untouchedLoopWithPath(5,4,b,a,P)
#l1,l2=UnTouchedLoops(8, 5, b, a)
#getDelta(l1,l2)
#deltaFrom1ToM(8, 5,2, b, a,Ps)
#print(getTransferFunction(5, 2,2, b,arrayOfPaths, a,Ps))
graph = [
    [(1, 1)],
    [(2, 2), (3, 4)],
    [(0, 3)],
    [(1, 5)]
]
graph2=[
    [(1,1)],
    [(2,5),(5,10)],
    [(3,10)],
    [(2,-1),(4,2)],
    [(1,-1),(3,-2),(6,1)],
    [(4,2),(5,-1)],
    [],
]
#result = forward_paths(graph2)
#print(result)
#compile(result,7)
print(forward_paths(graph2))
print(pipLine(graph2))

