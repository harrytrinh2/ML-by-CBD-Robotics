L =['2', '9', '10', '4', '3', '7', '1']
nextC = []
sophantu = len(L)
def sinhtapC(L,k):
    nextC=[]
    sophantu=len(L)
    if k==1:
        for i1 in range(0,(sophantu-1)):
            for i2 in range(i1+1,sophantu):
                nextC.append(frozenset([L[i1],L[i2]]))
    elif k>=2:
            for i1 in range(0,(sophantu-1)):
                for i2 in range(i1+1,sophantu):
                    L1=list(L[i1])[0:(k-1)]
                    L2=list(L[i2])[0:(k-1)]
                    print("L1 {} \nL2 {}".format(L1,L2))
                    L1.sort()
                    L2.sort()
                    if L1==L2:
                       temp= list(L[i1] | L[i2])
                       thoadk=True
                       for item in temp:
                            temp1=[x for x in temp if x != item]
                            if frozenset(temp1) not in L:
                                thoadk=False
                                break
                       if thoadk:
                            nextC.append(frozenset(temp))
    return nextC
k = 2
while L != []:
    C = sinhtapC(L, k - 1)