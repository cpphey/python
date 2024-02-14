import copy
input=[0,1,2]
ps=[[]]

#print(len(ps))
#exit(0) exit code

def oneDimensionalCopy(argList):
    ret=[]
    for idx in range(len(argList)):
        ret.append(argList[idx])
    return ret

def twoDimensionalCopy(argList):
    ret=[]
    for idx in range(len(argList)):
        ret.append(oneDimensionalCopy(argList[idx]))
    return ret

def makePowerset(arg):
    global ps #global variable
    #orig=ps.copy() #wont work as need deep copy https://stackoverflow.com/questions/2541865/copying-nested-lists-in-python
    orig=copy.deepcopy(ps) #orig=twoDimensionalCopy(ps)#[oneDimensionalCopy(x) for x in ps]
    toAdd=copy.deepcopy(orig) #toAdd=orig=twoDimensionalCopy(orig)#[oneDimensionalCopy(x) for x in orig]
    for idx in range(len(toAdd)):
        toAdd[idx].append(arg)
    added=orig+toAdd
    ps=added

for i in input:
    makePowerset(i)


temp1=10