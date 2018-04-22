import os
import sys
import operator

def cal_Min_Sup(s,minSupp):
    file= open(s,mode='r',encoding='utf8')
    C1={}
    Real_line=0
    for line in file:
        Real_line+=1
        for item in line.split(","):
            if item != "" and item != "\n":
                for i in item:
                    if i !="\n":
                        if i in C1:
                            C1[i] += 1
                        else:
                            C1[i] = 1
    minSupp1=round(minSupp/100 * Real_line)
    for key, value in C1.items():
        if int(value) <minSupp1:
            del C1[key]
    sorted_keys = sorted(C1, key=C1.get, reverse=True)
    d={}
    for r in sorted_keys:
        d[r] = C1[r]
    return (d)
def Ordered_items(s,item_list):
    file= open(s,mode='r',encoding='utf8')
    output_file = open("Fp-Tree_Output","w+")
    for line in file:
        for key, value in item_list.items():
            for item in line:
                if key == item:
                    output_file.write(key+",")
        output_file.write("\n")
    output_file.close()

if __name__ == "__main__":
    filename=input('Please enter file name: ')
    while True:
        try:
            minSupport = int(input('Please enter minimum support(%): '))
            break
        except ValueError:
            print('Min Support is a number!!!')
    dirname, tenfile = os.path.split(os.path.abspath(sys.argv[0]))
    s = os.path.join(dirname, filename)
    Item_List = []
    Item_List =cal_Min_Sup(s,minSupport)
    print("C1 = {0} {1}".format(Item_List,Ordered_items(s,Item_List)))
