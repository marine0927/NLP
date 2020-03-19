import sys,io
import re
from collections import Counter


# def dealline(line):
#     a=line.find('-')
#     b=line.find('_')
#     c=line.find('|')
#     d=line.find('—')
#     if a>-1 or b>-1 or c>-1 or d>-1:
#         return line[0:max(a,b,c,d)]
#     else:
#         return line
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
#
#
# with open('processed_res_2019_03_01.txt', 'r',encoding='utf-8-sig') as f:
#     content = f.read().splitlines()
#     c= Counter()
#     i=0
#     print (len(content))
#     for line in content:
#
#         str_list = line.split()
#         c[dealline(str_list[1])]+=1
#     print (c.most_common())


# a='123.123%'
# pattern = re.compile(r'^(\d+(\.\d+)?)((%)?)$')
# result = pattern.match(a)
# if result:
#     print (1)
print ((0.7992971119800197+0.7606064241670757+0.7594147649529135+0.5928213687695785+0.43122706242970255+0.38339885805009233+0.3487951457226828+0.34626335872427927+0.332796372460302+0.33006641108681434)/15)
print ((0.7992971119800197+0.7606064241670757+0.7594147649529135)/7)