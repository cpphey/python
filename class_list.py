class Test:
    def __init__(self):
        self.name='default'
        self.age=10

#    def __init__(self,arg1,arg2):
#        self.name=arg1
#        self.age=arg2

    def __str__(self):
        return f"{self.name} and {self.age}"


obj=Test()
print(obj)
#obj2=Test('haha',20)
#print(obj2)


def asd():
    my_list = [10, 20, 30, 40, 50]
    subset = my_list[1:4]
    return subset

i=asd()


aa=[0,1,2]
bb=[x + 2 for x in aa]
c=bb.count(2)
i=10