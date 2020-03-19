from sklearn import datasets
from sklearn import svm
import random
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from sklearn.externals import joblib
import numpy
import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
#调整了格式，一行是一条数据
def inputdata(filename):
    f = open(filename,'r',encoding='utf-8-sig')
    linelist = f.readlines()
    return linelist

def splitset(trainset,testset):
    train_words = []
    train_tags = []
    test_words = []
    test_tags = []
    for i in trainset:
        i = i.strip()
        # index = i.index(':')
        train_words.append(i[:-2])
        train_tags.append(int(i[-1]))


    for i in testset:
        i = i.strip()
        # index = i.index(':')
        test_words.append(i[:-2])
        test_tags.append(int(i[-1]))


    return train_words,train_tags,test_words,test_tags

#完成打开文件后的准备工作

comma_tokenizer = lambda x: jieba.cut(x, cut_all=True)

def tfvectorize(train_words,test_words):
    v = TfidfVectorizer(tokenizer=comma_tokenizer,binary = False, decode_error = 'ignore',stop_words = 'english')
    train_data = v.fit_transform(train_words)
    test_data = v.transform(test_words)
    return train_data,test_data

#按比例划分训练集与测试集
def splitDataset(dataset,splitRatio):
    trainSize = int(len(dataset)*splitRatio)
    trainSet = []
    copy = dataset
    while len(trainSet)<trainSize:
        index = random.randrange(len(copy))
        trainSet.append(copy.pop(index))
    return trainSet,copy

#得到准确率和召回率
def evaluate(actual, pred):
    m_precision = metrics.precision_score(actual, pred,average='macro')
    m_recall = metrics.recall_score(actual,pred,average='macro')
    print ('precision:{0:.3f}'.format(m_precision))
    # print ('recall:{0:0.3f}'.format(m_recall))

#创建svm分类器
def train_clf(train_data, train_tags):
    clf = svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3,
                  gamma='auto', kernel='linear', max_iter=-1, probability=False, random_state=None, shrinking=True,
                  tol=0.001, verbose=False)
    clf.fit(train_data, numpy.asarray(train_tags))

    return clf

def covectorize(train_words,test_words):
        v = CountVectorizer(tokenizer=comma_tokenizer,binary = False, decode_error = 'ignore',stop_words = 'english')
        train_data = v.fit_transform(train_words)
        test_data = v.transform(test_words)
        return train_data,test_data

if __name__ == '__main__':
        linelist = inputdata('data.txt')
        # for i in linelist:
        #     print i.decode('utf-8')

        # 划分成两个list
        # trainset, testset = splitDataset(linelist, 0.65)
        trainset=linelist[0:700]
        testset = linelist[700:]
        # for i in trainset:
        #     print i.decode('utf-8')
        # print('train number:', len(trainset))
        # print('test number:', len(testset))

        train_words, train_tags, test_words, test_tags = splitset(trainset, testset)
        c = train_words
        # train_data, test_data = tfvectorize(train_words, test_words)
        train_data, test_data = tfvectorize(train_words, test_words)
        # for i in test_data:
        #     print i
        clf = train_clf(train_data, train_tags)
        re = clf.predict(test_data)
        evaluate(numpy.asarray(test_tags), re)
        print (re)
        joblib.dump(clf,'clf.pkl')

        a = ['钱塘江大潮如约而至市民聚集江岸', '美媒：美军将在5年内试飞多斗机|战斗机|试飞_新浪军事_新浪网','战役“BBA”与保时捷竟然在这件事上争的不可开交_搜狐汽车_搜狐网']
        v = TfidfVectorizer(tokenizer=comma_tokenizer, binary=False, decode_error='ignore', stop_words='english')
        train_data = v.fit_transform(c)
        b=v.transform(a)
        clf2=joblib.load('clf.pkl')
        tolist=clf2.predict(b)
        print(tolist)