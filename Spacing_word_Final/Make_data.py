import pandas as pd

with open('ml_6_spacing_train.csv') as file:
    data=[]
    for line in file.readlines():
        temp=line.split(',')
        if temp[3]=='\n':
            temp[3]=None
        data.append(temp)
data.pop(0)
n=0
for i in data:
    n=max(n,len(i[0]))
test=[]
with open('ml_6_spacing_test.csv') as file:
    for line in file.readlines():
        test.append(line[:len(line)-1])
test.pop(0)
for i in test:
    n=max(n,len(i))
new=[]
for word in data:
    temp=[]
    num=0
    for j in range(len(word[0])):
        if word[0][j] in ["a","e","i","o","u"]:
            num+=1
            temp.append(ord(word[0][j])+1000)
        else:
            temp.append(ord(word[0][j]))
    if len(temp)<n:
        temp+=[-1]*(n-len(temp))
    temp.append(len(word[0]))
    temp.append(num)
    temp.append(len(word[1]))
    new.append(temp)

for word in test:
    temp=[]
    num=0
    for j in range(len(word)):
        if word[j] in ["a","e","i","o","u"]:
            num+=1
            temp.append(ord(word[j])+1000)
        else:
            temp.append(ord(word[j]))
    if len(temp)<n:
        temp+=[-1]*(n-len(temp))
    temp.append(len(word[0]))
    temp.append(num)
    new.append(temp)


res = pd.DataFrame(new)
res.to_csv("word_v3_last.csv")
