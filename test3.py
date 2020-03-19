import itertools
import copy
import pymysql
'''
定义全局变量k，即支持度计数k,此k也可以在运行程序之前输入，简单改动即可
'''
global k
k = 0

'''
存储频繁项集的列表
'''
frequenceItem = []

'''
从txt文件dataset.txt里获取事务集
'''


def getDataSet(id):
    name = 'root'
    password = 'wasd5123'  # 替换为自己的账户名和密码
    # 建立本地数据库连接(需要先开启数据库服务)
    db = pymysql.connect('localhost', name, password, charset='gbk')
    cursor = db.cursor()
    sqlSentence2 = "use lhb;"
    cursor.execute(sqlSentence2)
    sqlSentence4 = "select 数据 from stock_"+ id +";"
    cursor.execute(sqlSentence4)
    results = cursor.fetchall()



    dataset = []
    for line in results:
        line=''.join(line)
        temp1 = line.strip('\r\n')
        temp2 = temp1.split(',')
        for x in temp2:
            if x=='':
                temp2.remove('')
        dataset.append(temp2)
    global k
    k=(len(dataset))*0.4
    return dataset


'''
初步扫描事务集，从事务集里获取候选1项集
方法的基本思路是：
定义一个集合tmp，将事务集的第一项作为tmp的初始集合
然后扫描事务集，将不在tmp里的数据项加入tmp中
'''


def find_item(dataset):
    length = len(dataset)
    for i in range(0, length):
        if i == 0:
            tmp = set(dataset[i])
        tmp.update(set(dataset[i]))
    candidate = list(tmp)
    candidate.sort()
    return candidate


'''
从候选项集里找出频繁项集，其中num代表频繁num+1项集
如num为0的为从候选1项集里找出频繁1项集
方法基本思路：
1、定义一个支持度列表count
2、对于每一个候选项，依次扫描事务集，如果该项出现在事务集中就将该项对应的count+1、定义一个支持度列表count+1 
3、将每一项的count和k（支持度计数）进行比较，将count小于k的项剔除
'''


def find_frequent(candidate, dataset, num):

    frequence = []
    length = len(candidate)
    count = []
    for i in range(0, length):
        count.append(0)
        count[i] = 0
        if num == 0:
            child = set([candidate[i]])
        else:
            child = set(candidate[i])
        for j in dataset:
            parent = set(j)
            if child.issubset(parent):
                count[i] = count[i] + 1
    for m in range(0, length):
        if count[m] >= k:
            frequence.append(candidate[m])
    return frequence


'''
其实不管num为0还是别的值算法应该是一样的，但是由于程序实现上的问题
num为0的时候选项集是一维列表，其它的时候，候选项集是二维列表，
毕竟只是自己写着玩的，python还不熟，牵一发而动全身，懒得改了
'''


'''
先验定理，剪枝掉不必要的候选n项集
方法思路：
1、依次取出候选项集里的项
2、取出n项集里的n-1项子集
3、如果所有的n-1项集不都都是频繁n-1项集的子集，则删除该候选项集
'''


def pre_test(candidate, num, frequence):
    r_candidate = copy.deepcopy(candidate)
    for each in candidate:
        for each2 in itertools.combinations(each, num):
            tmp = (list(each2))
            tag = 0
            for j in frequence:
                if num == 1:
                    if (tmp[0] == j):
                        tag = 1
                        break
                else:
                    if tmp == j:
                        tag = 1
                        break
            if tag == 0:
                r_candidate.remove(each)
                break
    return r_candidate


'''
通过频繁n-1项集产生候选n项集，并通过先验定理对候选n项集进行剪枝
方法思路：
1、如果是频繁1项集，则通过笛卡尔积产生频繁2项集
2、如果不是频繁一项集，采用F（k-1） * F（k-1）方法通过频繁n-1项集产生候选n项集
注：F（k-1） * F（k-1）方法在我的另一篇关联算法博客上做了理论上的简单介绍，或者也可以直接参看《数据挖掘导论》
'''


def get_candidata(frequence, num):
    length = len(frequence)
    candidate = []
    if num == 1:
        for each in itertools.combinations(frequence, 2):
            tmp = list(each)
            tmp3 = []
            tmp3.append(tmp[0])
            tmp3.append(tmp[1])
            candidate.append(tmp3)
    else:
        for i in range(0, length - 1):
            tmp1 = copy.deepcopy(frequence[i])
            tmp1.pop(num - 1)
            for j in range(i + 1, length):
                tmp2 = copy.deepcopy(frequence[j])
                tmp2.pop(num - 1)
                if tmp1 == tmp2:
                    tmp3 = copy.deepcopy(frequence[i])
                    tmp3.append(frequence[j][num - 1])
                    candidate.append(tmp3)
    candidate2 = pre_test(candidate, num, frequence)
    return candidate2


'''
main程序
'''
if __name__ == '__main__':

    with open('stockid.txt', 'r') as f:
        content = f.read().splitlines()
        for line in content:
            print (line)

            dataset = getDataSet(line)
            if dataset==[]:
                print ("集合为空")
                continue
            if(len(dataset))<10:
                print ("长度不够")
                continue
            Item = find_item(dataset)
            num = 0
            frequenceItem = []

            while 1:
                if num == 0:
                    candidate = Item
                else:
                    candidate = get_candidata(frequenceItem[num - 1], num)
                frequenceItem.append(find_frequent(candidate, dataset, num))
                if frequenceItem[num] == []:
                    frequenceItem.pop(num)
                    break
                num = num + 1

            if len(frequenceItem)>1:
                name = 'root'
                password = 'wasd5123'  # 替换为自己的账户名和密码
                # 建立本地数据库连接(需要先开启数据库服务)
                db = pymysql.connect('localhost', name, password, charset='gbk')
                cursor = db.cursor()
                sqlSentence2 = "use lhb;"
                cursor.execute(sqlSentence2)
                a=str(frequenceItem[1])
                a=a.replace("'", "\\'")
                print (a)
                sqlSentence4 = "replace into stockdata (id,couples) values ('%s','%s')" % (line, a)
                cursor.execute(sqlSentence4)
                cursor.close()
                db.commit()
                db.close()



