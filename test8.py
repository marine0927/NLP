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

with open('特斯拉.txt', 'r',encoding='utf-8-sig') as f:
    content = f.read().splitlines()
    a=0
    b=0
    c=0
    d=0
    for i in range(1000):
        line=content[i]
        str_list = line.split()
        if((str(str_list[0])=='1')&(str(str_list[1])=='True')):
            a=a+1
        if((str(str_list[0])=='1')&(str(str_list[1])=='False')):
            b=b+1
        if((str(str_list[0])=='0')&(str(str_list[1])=='True')):
            c=c+1
        if((str(str_list[0])=='0')&(str(str_list[1])=='False')):
            d=d+1
        print (i-(a+b+c+d),i)

    print (a,b,c,d)
