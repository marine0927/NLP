import sys,io
import string
import jieba
import jieba.analyse
import numpy
import math
import re
from collections import Counter
import matplotlib.pyplot as plot




sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

stopwords = [line.strip() for line in open('stopwords.txt', 'r', encoding='gb18030').readlines()]



#去后缀
def dealline(line):
    a=line.find('-')
    b=line.find('_')
    c=line.find('|')
    d=line.find('—')
    if a>-1 or b>-1 or c>-1 or d>-1:
        return line[0:max(a,b,c,d)]
    else:
        return line


#提取标题
with open('processed_res_2019_03_01.txt', 'r',encoding='utf-8-sig') as f:
#     content = f.read().splitlines()
#     for line in content:
#         str_list = line.split()
#         with open('title.txt', 'a', encoding='utf-8-sig') as t:
#              t.write(str_list[1]+'\t'+str_list[2] + '\n')

# with open('title.txt', 'r',encoding='utf-8-sig') as f:
#     content = f.read().splitlines()



    i=0
    j=0
    titlelist=[]
    detitlelist=[]
    content = f.read().splitlines()

    #2000条人工智能4000条非人工智能
    for line in content:

        str_list = line.split()
        if str_list[1].find('特斯拉') != -1:

            if i < 4900:
                titlelist.append(dealline(str_list[2]))
                i=i+1
            else:
                continue
        else:
            if j<60000:
                detitlelist.append(dealline(str_list[2]))
                j = j + 1
            else:
                continue

    c0= Counter()
    c1=Counter()
    c2=Counter()

    for item in titlelist:
        for word in list(set(jieba.lcut_for_search(item))):
            c1[word]+=1
            c2[word]+=0


    for item in detitlelist:
        for word in list(set(jieba.lcut_for_search(item))):
            c2[word]+=1
            c1[word]+=0
    for word in stopwords:
        del c2[word]
        del c1[word]

    for (k,v) in c1.most_common():
        a=c1[k]
        b=c2[k]
        c=(4900-c1[k])
        d=60000-c2[k]
        c0[k]=(a*d-b*c)/math.sqrt((a+b)*(d+c)*10000)

    ranklist=Counter()


    #归一化
    maxi=c0.most_common()[0][1]
    mini=c0.most_common()[len(c0.most_common())-1][1]
    for (k,v) in c0.most_common():
        c0[k]=(c0[k]-mini)/(maxi-mini)-(0-mini)/(maxi-mini)
        pattern = re.compile(r'^(\d+(\.\d+)?)((%)?)$')
        result = pattern.match(k)
        if result:
            del c0[k]
    # for (k,v) in c0.most_common():
    #     if k[len(k)-1]=='网':
    #         print(k)


    # for (k, v) in c0.most_common():
    #     with open('共享单车.txt', 'a', encoding='utf-8-sig') as t:
    #          t.write(k+'\t'+ str(v) + '\n')


    print(c0.most_common(200))
    with open('test.txt', 'r', encoding='utf-8-sig')as f:
        context = f.read().splitlines()
        i = 0
        for line in context:
            line=dealline(line)
            seg_list = jieba.cut_for_search(line)
            # print(line)
            toplist = []
            detoplist=[]
            for element in seg_list:
                if c0[element]>0:
                    # print(element,c0[element])
                    toplist.append(c0[element])
                if c0[element]<0:
                    detoplist.append(c0[element])
            toplist.sort(reverse=True)
            detoplist.sort()
            print (detoplist)
            ranklist[line]=0
            if len(toplist)>0:
                if len(toplist) > 3:
                    ranklist[line] += (toplist[0] + toplist[1] + toplist[2])
                else:
                    ranklist[line] += numpy.sum(toplist)
            if len(detoplist)>0:
                if len(detoplist) > 3:
                    ranklist[line] += (detoplist[0] + detoplist[1] + detoplist[2])
                else:
                    ranklist[line] += numpy.sum(detoplist)

     #得出的ranklist（line)就是权值

#画图
# plot.figure()
x=0
for (k, v) in ranklist.most_common():
    x=x+1
    y=v
    # plot.scatter(x,y)
    print(k, v)
# plot.show()
print (c1['美股'],c2['美股'])
#阈值设定为
print ((c0.most_common()[0][1]+c0.most_common()[1][1]+c0.most_common()[2][1])/7)

line='E周刊|马斯克来华挖洞缓解拥堵史上最便宜的布加迪即将问世_搜狐汽车_搜狐网'
line = dealline(line)
seg_list = jieba.cut_for_search(line)
for element in seg_list:
    print (element,c0[element])





