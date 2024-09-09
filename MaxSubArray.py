import copy


#-------------------------------------------------------------------------
# Generate Contigous Subsets
#-------------------------------------------------------------------------
subsets = set()


def findContigousSubsets(arg, addCallsMade):
    if len(arg) == 1:
        return arg
    else:
        # Full added
        subsets.add(arg)
        addCallsMade += 1

        # Left added
        subsets.add(arg[0])
        addCallsMade += 1
        findSubs(arg[1:])

        # Right added
        subsets.add(arg[-1])
        addCallsMade += 1
        findSubs(arg[:-1])

        return addCallsMade


addCallsMade = findContigousSubsets("ABCDE", 0)
print(subsets)
print(addCallsMade)
print(len(subsets))

#-------------------------------------------------------------------------
# JUST RESULT
#-------------------------------------------------------------------------
def subMax1(argList):
    if len(argList) == 1:
        return argList[0]
    else:
        return max(sum(argList),subMax(argList[1:]),subMax(argList[:-1]))

subMax1([5,4,-1,7,8])
subMax1([-2,1,-3,4,-1,2,1,-5,4])

#-------------------------------------------------------------------------
# WITH BACKTRACKING
#-------------------------------------------------------------------------
def AbhiMax (arg1, arg2, arg3):
    num = max(arg1[0],arg2[0],arg3[0])
    arr=[]
    if num == sum (arg1[1]):
        arr = arg1[1]
    elif num == sum (arg2[1]):
        arr = arg2[1]
    elif num == sum (arg3[1]):
        arr = arg3[1]

    return (num,arr)

def subMax(argList, arr):

    if len(argList) == 1:
        return (argList[0] , [argList[0]] )
    else:
        return AbhiMax( (sum(argList),argList),  subMax(argList[1:],argList[1:]) ,  subMax(argList[:-1],argList[:-1])  )



# result=subMax([5,4,-1,7,8])
result, arr = subMax([-2, 1, -3, 4, -1, 2, 1, -5, 4] , [] )
# result=subMax([1])
print(result)
print(arr)