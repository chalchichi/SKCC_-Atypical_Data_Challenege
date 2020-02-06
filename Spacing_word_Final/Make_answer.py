import pandas as pd
import math
with open('word_nox.csv') as file:
    dic=[]
    for line in file.readlines():
        dic.append(line[:len(line)-1])

with open('ml_6_spacing_train3.csv') as file:
    data=[]
    for line in file.readlines():
        temp=line.split(',')
        if temp[3]=='\n':
            temp[3]=None
        data.append(temp)
        dic.append(temp[1])
        dic.append(temp[2])
data.pop(0)
n=0
for i in data:
    n=max(n,len(i[0]))
new=[]
def make(word):
    temp = []
    for j in range(len(word)):
        if word[j]=="a":
            temp.append(ord("a"))
        elif word[j]=="e":
            temp.append(ord("e"))
        elif word[j]=="i":
            temp.append(ord("i"))
        elif word[j]=="o":
            temp.append(ord("o"))
        elif word[j]=="u":
            temp.append(ord("u"))
        else:
            temp.append(-1)
    if len(temp) < n:
        temp += [0] * (n - len(temp))
    return temp


for word in data:
    l=make(word[0])
    new.append(l)

def simul(a,b):
    d=0
    d2=0
    d3=0
    for i in range(len(a)):
        d+=a[i]*a[i]
        d2+=b[i]*b[i]
        d3+=a[i]*b[i]
    if d2==0 or d==0:
        return 0
    return d3/(math.sqrt(d)*math.sqrt(d2))
#data,n,new 지역변수

def sp(word):
    a_array=make(word)
    ans=[]
    for i in range(1500):
        co=simul(a_array,new[i])
        ans.append([data[i],co])
    ans=sorted(ans,key=lambda x:x[1],reverse=True)
    return ans[0:5],len(ans[0][0][1])

total=[]
answer=0
def check(word):
    if word in dic:
        return True
    else:
        return False
ans=[]
for i in range(1500,2000):
    l,s=sp(data[i][0])
    if check(data[i][0][:s])==True and check(data[i][0][s:])==True:
        s=s
    else:
        if check(data[i][0][:s-1])==True and check(data[i][0][s-1:])==True:
            s-=1
        elif check(data[i][0][:s+1])==True and check(data[i][0][s+1:])==True:
            s+=1
        else:
            if check(data[i][0][:s - 2]) == True and check(data[i][0][s - 2:]) == True:
                s -= 2
            elif check(data[i][0][:s + 2]) == True and check(data[i][0][s + 2:]) == True:
                s += 2
            else:
                if check(data[i][0][:s - 3]) == True and check(data[i][0][s - 3:]) == True:
                    s -= 3
                elif check(data[i][0][:s + 3]) == True and check(data[i][0][s + 3:]) == True:
                    s += 3

    ans.append([data[i][0],data[i][0][:s],data[i][0][s:]])
ans2=ans
with open('word_nox.csv') as file:
    dic=[]
    for line in file.readlines():
        dic.append(line[:len(line)-1])

with open('ml_6_spacing_test.csv') as file:
    data=[]
    for line in file.readlines():
        data.append(line[:len(line)-1])
data.pop(0)
with open('ml_6_spacing_train.csv') as file:
    for line in file.readlines():
        l=line.split(",")
        dic.append(l[1])
        dic.append(l[2])

with open('last.csv') as file:
    cri=[]
    for line in file.readlines():
        cri.append(round(float(line[:len(line)-1])))

def make(word):
    temp = []
    for j in range(len(word)):
        if word[j]=="a":
            temp.append(ord("a"))
        elif word[j]=="e":
            temp.append(ord("e"))
        elif word[j]=="i":
            temp.append(ord("i"))
        elif word[j]=="o":
            temp.append(ord("o"))
        elif word[j]=="u":
            temp.append(ord("u"))
        else:
            temp.append(-1)
    if len(temp) < n:
        temp += [0] * (n - len(temp))
    return temp


total=[]
answer=0
def check(word):
    if word in dic:
        return True
    else:
        return False
ans=[]
for i in range(500):
    s=cri[i]
    if check(data[i][:s])==True and check(data[i][s:])==True:
        s=s
    else:
        if check(data[i][:s-1])==True and check(data[i][s-1:])==True:
            s-=1
        elif check(data[i][:s+1])==True and check(data[i][s+1:])==True:
            s+=1
        else:
            if check(data[i][:s - 2]) == True and check(data[i][s - 2:]) == True:
                s -= 2
            elif check(data[i][:s + 2]) == True and check(data[i][s + 2:]) == True:
                s += 2
            else:
                if check(data[i][:s - 3]) == True and check(data[i][s - 3:]) == True:
                    s -= 3
                elif check(data[i][:s + 3]) == True and check(data[i][s + 3:]) == True:
                    s += 3
                else:
                    if check(data[i][:s - 4]) == True and check(data[i][s - 4:]) == True:
                        s -= 4
                    elif check(data[i][:s + 4]) == True and check(data[i][s + 4:]) == True:
                        s += 4
    if data[i][s:]=="":
        for k in range(s//2,len(data[i])):
            if check(data[i][k:])==True:
                s=k
                break
    if data[i][:s]=="":
        s=len(ans2[i][1])
    if len(data[i][:s])==1 or len(data[i][s:])==1:
        if len(ans2[i][1])==1 or len(ans2[i][2])==1:
            s=len(data[i])//2
        else:
            s=len(ans2[i][1])
        print(data[i],data[i][:s],data[i][s:])
    ans.append([data[i],data[i][:s],data[i][s:]])
dataframe=pd.DataFrame(ans)
dataframe.to_csv("answer.csv")
