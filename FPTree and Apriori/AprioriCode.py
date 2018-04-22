import os
import sys
def Cal_Support(s,minsupport):
    file = open(s,mode='r',encoding='utf8')
    C1={} #declare a dictionary
    for line in file:
      for item in line.split(';'):
          if item!='' and item !='\n':
             if item in C1:
                 C1[item]+=1
             else:
                 C1[item]=1
    L1=[]
    for item in C1:
        if C1[item]>=minsupport:
            L1.append(item)
    print("C1 {} \nL1 {}".format(C1,L1))
    return sorted(L1)


def sinhtapC(L, k):
    nextC = []
    sophantu = len(L)
    if k == 1:
        for i1 in range(0, (sophantu - 1)):
            for i2 in range(i1 + 1, sophantu):
                nextC.append(frozenset([L[i1], L[i2]]))
    elif k >= 2:
        for i1 in range(0, (sophantu - 1)):
            for i2 in range(i1 + 1, sophantu):
                L1 = list(L[i1])[0:(k - 1)]
                L2 = list(L[i2])[0:(k - 1)]
                L1.sort()
                L2.sort()
                if L1 == L2:
                    temp = list(L[i1] | L[i2])
                    thoadk = True
                    for item in temp:
                        temp1 = [x for x in temp if x != item]
                        if frozenset(temp1) not in L:
                            thoadk = False
                            break
                    if thoadk:
                        nextC.append(frozenset(temp))

    return nextC


if __name__=="__main__":
    filename=input('Enter your filename: ')
    while True:
        try:
            minSupport_Value=int(input('Your Minsupport is: '))
            break
        except ValueError:
            print('Failed! please enter integer data type! ')
    dirname,tenfile=os.path.split(os.path.abspath(sys.argv[0]))
    s=os.path.join(dirname, filename)
    L=Cal_Support(s,minSupport_Value)
