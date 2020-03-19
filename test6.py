import sys,io
import string
import jieba
import jieba.analyse
import numpy
import math
from collections import Counter


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


# with open('processed_label2w.txt', 'r',encoding='utf-8-sig') as f:
#     i=0
#     titlelist=''
#     detitlelist=''
#     content = f.read().splitlines()
#
#     for line in content:
#         if line.find('特斯拉') != -1:
#             str_list = line.split()
#             if i < 1000:
#                 print(str_list[2])
#                 with open('tsl.txt', 'a', encoding='utf-8-sig') as t:
#                     t.write(str_list[2] + '\n')
#                 i=i+1




cgroup=[]


titlelist=('rgzn','yjzz','xnyqc','ydyl','tsl','zzlr','ygadwq','zccz','gqzr','gsgl')
for title in titlelist:
    with open(title+'.txt', 'r', encoding='utf-8-sig')as f:
        txt = f.read()
        seg_list = jieba.cut(txt)
        c = Counter()
        for x in seg_list:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1
        cgroup.append(c.most_common())

c=Counter()
ctfidflist=[]
for topic in cgroup:
    for (k,v) in topic:
        c[k]+=1
for (k,v) in c.most_common():
    print(k,v)

for i in range(10):
    ctfidf = Counter()
    print(titlelist[i])
    for (k,v) in cgroup[i]:
        ctfidf[k]=(v/1000)*(math.log(10/c[k],10))
    ctfidflist.append(ctfidf)

for (k,v) in ctfidflist[0].most_common():
    print(k,v)

ranklist1=Counter()

with open('rgzn.txt', 'r', encoding='utf-8-sig')as f:
    context=f.read().splitlines()
    i = 0
    for line in context:
        sum=0

        seg_list = jieba.cut(line)
        for element in seg_list:
            sum+=ctfidflist[0][element]
        ranklist1[line]=sum/len(line)

for (k,v) in ranklist1.most_common():
    print(k,v)

