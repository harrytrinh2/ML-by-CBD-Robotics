import os
import sys
import datetime
  
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
                    print("L1 {} - L2 {}".format(L1,L2))
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

def tinhdohotro1(s,minsupport):
    file = open(s,mode='r',encoding='utf8')
    C1={}
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
    return sorted(L1)  

def tinhdohotroN(s,itemsCollectionC,minsupport,k):
    dict_supp={}
    for s1 in itemsCollectionC:
       # s1=frozenset(items)
        file = open(s,mode='r',encoding='utf8')
        for line in file:
            s2=line.split(';')
            if '\n' in s2: s2.remove('\n')
            s2= frozenset(s2)
            if s1.issubset(s2):
                if s1 in dict_supp:
                     dict_supp[s1]+=1
                else:
                     dict_supp[s1]=1
                if dict_supp[s1]>=minsupport: break      
                    
        file.close()
    
    nextL=[x for x in dict_supp if dict_supp[x]>=minsupport]

    dirname,filename_input=os.path.split(s)    
    output_file = open(os.path.join(dirname,'{0}_Supp{1}_output_ttx.txt'.format(filename_input[0:filename.rfind('.')],minsupport)),mode='a')
    for item in nextL:
        sapxep= list(item)
        sorted(sapxep)
        for k in sapxep:
          output_file.write(k)
          output_file.write(';')
        output_file.write('\n')
    output_file.close()    
    return sorted(nextL)

        #============== MAIN PROGRAM ======================

filename=input('Nhap ten tap tin du lieu: ')
while True:
    try:
        nguongtoithieu=int(input('Nhap nguong toi thieu: '))
        break
    except ValueError:
        print('Vui long nhap so nguyen.')
dirname,tenfile=os.path.split(os.path.abspath(sys.argv[0]))
s=os.path.join(dirname, filename)
L=tinhdohotro1(s,nguongtoithieu)
if len(L)==0:
      print('Trong Co so du lieu giao tac khong co muc du lieu thuong xuyen thoa nguong toi thieu {0}'.format(nguongtoithieu))
else:
    output_file = open(os.path.join(dirname,'{0}_Supp{1}_output_ttx.txt'.format(filename[0:filename.rfind('.')],nguongtoithieu)),mode='w')
    for item in L:
        output_file.write(item)
        output_file.write(';\n')
    output_file.close()
    k=2
    while L!=[]:
        C=sinhtapC(L,k-1)
        L=tinhdohotroN(s,C,nguongtoithieu,k)
        k+=1

