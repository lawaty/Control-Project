import numpy as np
import sympy as sp

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
#output:
#       the transferFunction
#       easy to edit and return any step of this steps  (delta,delta from 1 to m,combination of untouched loops)

def UnTouchedLoops(numOfNodes, numOfLoops, arrayOfLoops, nodesInLoops):
    for i in range(numOfLoops):
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




    return arrayOfLoops,numOfUntouched

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
                    print(nodesInLoops[i])             
     return newArrayOfLoops,newNodesInLoops     

def getDelta(arrayOfLoops,numOfUntouched):
    #print (type(arrayOfLoops))
    
    result = sp.Integer(1)
    for i in range (len(arrayOfLoops)):
          print(arrayOfLoops[i])
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
            l3,l4=UnTouchedLoops(numOfNodes, len(l1),l1,l2)
            deltas[i]=getDelta(l3,l4)
        i +=1
     return deltas  

def getTransferFunction(numOfNodes, numOfLoops,numOfPaths, arrayOfLoops,arrayOfPaths, nodesInLoops,nodesInPaths):
     deltas=deltaFrom1ToM(numOfNodes, numOfLoops,numOfPaths, arrayOfLoops, nodesInLoops,nodesInPaths)
     l1,l2=UnTouchedLoops(numOfNodes, numOfLoops, arrayOfLoops, nodesInLoops)
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
     print(result)   
# Test data
a = np.array([[0,0,1,1,0], [0,1,1,1,0]])
b = ["-g2*h1", "-g1*g2*h2"]
Ps=np.array([[1,1,1,1,1],[1,0,1,1,1]])
arrayOfPaths = ["g1*g2","g2"]
# Call the function
#untouchedLoopWithPath(5,4,b,a,P)
#l1,l2=UnTouchedLoops(8, 5, b, a)
#getDelta(l1,l2)
#deltaFrom1ToM(8, 5,2, b, a,Ps)
getTransferFunction(5, 2,2, b,arrayOfPaths, a,Ps)

