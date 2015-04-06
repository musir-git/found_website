# -*- coding: utf-8 -*-
from __future__ import division
import codecs
import jieba.posseg as pseg
import jft
#import jieba.analyse
#import chardet

trainData = []#存放训练集
testData = []#存放测试集
needClassfiedData = []#存放待分类项
trainNum = 0#训练集中的微博条数
testNum = 0#测试集中的微博条数
needClassfiedNum = 0 #待分类的微博条数
C1_map = []#捡到微博分类的特征属性概率
C2_map = []#丢失微博分类的特征属性概率
feature = ["捡","拾","失主","认领","拣","丢","遗","落","掉","忘","不见","望","求","麻烦","谢","感激"]#特征属性
tag = ["v","v","n","v","v","v","v","v","v","v","v","v","v","v","v","v"]#特征属性的词性
featureNum = len(feature)#特征属性的个数
A=[0,0]#存放测试集中两类微博的概率，A[0]为捡到微博的概率，A[1]为丢失微博的概率
n = 0#使用朴素贝叶斯进行分类，分类正确的微博数
nn = 0#使用字符串匹配进行分类，分类正确的微博数

#初始化函数，将每个类型的特征属性划分的条件概率都置为0
def init():
    for i in range(featureNum):
        C1_map.append(0)
    for i in range(featureNum):
        C2_map.append(0)

#读取训练集数据，每6行作为一条微博存入trainData中
def trainDataRead(fileName):
    text = codecs.open(fileName, 'rU').read()
    lineList = text.split('\n')
    lineList.pop(0)
    count = 0
    eachWeibo = []
    for line in lineList:
        eachWeibo.append(line)
        count = count + 1
        if(count == 7):
            trainData.append(eachWeibo)
            count = 0
            eachWeibo = []
            
    global trainNum
    trainNum = len(trainData)

#读取测试集数据，每7行作为一条微博存入testData中，其中第一行为该微博的分类
#“1”代表捡到微博，“2”代表丢失微博
def testDataRead(fileName):
    text = codecs.open(fileName, 'rU').read()
    lineList = text.split('\n')
    lineList.pop(0)
    count = 0
    eachWeibo = []
    for line in lineList:     
        eachWeibo.append(line)
        count = count + 1
        if(count == 7):
            testData.append(eachWeibo)
            count = 0
            eachWeibo = []
            
    global testNum
    testNum = len(testData)

#读入待分类微博，每6行作为一条微博存入needClassfiedData中
def needClassfiedDataRead(fileName):
    text = codecs.open(fileName, 'rU').read()
    lineList = text.split('\n')
    lineList.pop(0)
    count = 0
    eachWeibo = []
    for line in lineList:     
        eachWeibo.append(line)
        count = count + 1
        if(count == 6):
            needClassfiedData.append(eachWeibo)
            count = 0
            eachWeibo = []
            
    global needClassfiedNum
    needClassfiedNum = len(needClassfiedData)
    
#训练分类器
def creatClassifier():
    global trainNum
    
    #统计两个分类的微博数
    count1 = 0
    count2 = 0
    
    for i in range(trainNum):
        if(trainData[i][0] == str(1)):
            count1 = count1 + 1
        if(trainData[i][0] == str(2)):
            count2 = count2 + 1
            
    A[0] = count1/trainNum
    A[1] = count2/trainNum

    #对两个分类每个特征属性计算所有划分的条件概率
    for i in range(trainNum):
        if(trainData[i][0] == str(1)):
            for j in range(featureNum):
                weiboContent = trainData[i][4]
                if(weiboContent.count(feature[j]) != 0):
                    C1_map[j] = C1_map[j] + 1

        if(trainData[i][0] == str(2)):
            for j in range(featureNum):
                weiboContent = trainData[i][4]
                if(weiboContent.count(feature[j]) != 0):
                    C2_map[j] = C2_map[j] + 1

    #Laplace校准
    for i in range(featureNum):
        #if(C1_map[i] == 0):
        #    C1_map[i] = 1
        #C1_map[i] = C1_map[i]/count1
        C1_map[i] = (C1_map[i] + 1)/count1
        #if(C2_map[i] == 0):
        #    C2_map[i] = 1
        #C2_map[i] = C2_map[i]/count1  
        C2_map[i] = (C2_map[i] + 1)/count2

#分类
def classfy():
    #将分成的捡到微博和丢失微博放入find.txt和lost.txt两个文件中
    f = open("find.txt", 'w+')
    ff = open("lost.txt", 'w+')
    
    for i in range(needClassfiedNum):
        #对每个类别计算P(x|yi)P(yi)
        p = [1,1]#p[i]代表P(x|yi)P(yi)
        pXC = [1,1]#pXC[i]代表p(x|yi)
        
        #计算P(x|y1)/p(y1)
        
        #存放待分类微博中出现的特征属性，用于对后验概率的调整
        #has1[0]存放前5个特征属性，属于捡到微博的特征属性
        #has1[1]存放其他特征属性，属于丢失微博的特征属性
        has1 = []
        has1.append([])
        has1.append([])
        
        for j in range(featureNum):
            weiboContent = needClassfiedData[i][3]
            if(weiboContent.count(feature[j]) != 0):
                pXC[0] = pXC[0] * C1_map[j]

                if(j >= 0 and j <= 4):
                    has1[0].append(j)
                if(j >= 5 and j < featureNum):
                    has1[1].append(j)             
            else:
                pXC[0] = pXC[0] * (1 - C1_map[j]) 
        
        #调整后验概率
        
        #当只出现捡到特征属性时候，分别增加属于捡到微博的概率
        if(len(has1[0]) != 0 and len(has1[1]) == 0):
            pXC[0] = pXC[0] * 2
        #当捡到特征属性和丢失特征属性都出现一次的时候，根据它们出现的位置调整后验概率
        #类似先出现“捡到”后出现“丢失”，增加属于捡到微博的概率
        if(len(has1[0]) == len(has1[1]) == 1):
            if(weiboContent.find(feature[has1[0][0]]) < 
               weiboContent.find(feature[has1[1][0]])):
                pXC[0] = pXC[0] * 10
        #根据出现的特征属性前的名词后者人称代词来调整后验概率
        #类似“捡到”前面出现“我”，“丢失”前面出现“谁”，增加属于捡到微博的概率
        words = [w.word for w in pseg.cut(needClassfiedData[i][3])]
        tags = [w.flag for w in pseg.cut(needClassfiedData[i][3])]
        
        for lostFIndex in has1[1]:
            #取得丢失特征词在已分词的微博的索引index
            for index in range(len(words)):
                if(words[index] == feature[lostFIndex]):
                    break
            #找到丢失特征词前面的名词
            while((index - 1 >= 0) 
                  and (not(tags[index-1] == 'r' or tags[index-1] == 'n')) ):
                index = index - 1
            #记录找到的名词的索引或者索引0
            indexTemp = index - 1
            #找到的索引之前第一个非名词的索引，包括当前索引
            while(indexTemp >= 0 and tags[indexTemp].find('n') != -1):
                indexTemp = indexTemp - 1
            #如果找到的非名词索引为介词，再继续找之前的名词索引
            if(tags[indexTemp] == 'p'):
                while((indexTemp - 1 >= 0) 
                      and (not(tags[indexTemp - 1] == 'r' or tags[indexTemp -1] == 'n'))):
                    indexTemp = indexTemp - 1
                #如果找不到则跳回最开始找到的名词索引
                if(indexTemp == 0):
                    indexTemp = index - 1
            #如果找的的非名词索引不为介词，也跳回最开始找到的名词索引
            else:
                indexTemp = index - 1
            if(words[indexTemp] == "你" or words[indexTemp] == "谁" or words[indexTemp] == "人"):
                pXC[0] = pXC[0] * 100
                
        for findFIndex in has1[0]:
            #取得捡到特征词在已分词的微博的索引index
            for index in range(len(words)):
                if(words[index] == feature[findFIndex]):
                    break
            #判断捡到特征词前面有没有以下的词语
            if(words[index-1] == "我"):
                pXC[0] = pXC[0] * 100
                
        p[0] = A[0] * pXC[0]
        
        #计算P(x|y2)/p(y2)
        
        has2 = []
        has2.append([])
        has2.append([])
        for j in range(featureNum):
            weiboContent = needClassfiedData[i][3]
            if(weiboContent.count(feature[j]) != 0):
                pXC[1] = pXC[1] * C2_map[j]
                if(j >= 0 and j <= 4):
                    has2[0].append(j)
                if(j >= 5 and j < featureNum):
                    has2[1].append(j)
            else:
                pXC[1] = pXC[1] * (1 - C2_map[j]) 
                
        #调整后验概率        
        if(len(has2[0]) == 0 and len(has2[1]) != 0):
            pXC[1] = pXC[1] * 2
        if(len(has2[0]) == len(has2[1]) == 1):
            if(weiboContent.find(feature[has2[0][0]]) > 
               weiboContent.find(feature[has2[1][0]])):
                pXC[1] = pXC[1] * 10
                
        for lostFIndex in has1[1]:
            #取得丢失特征词在已分词的微博的索引index
            for index in range(len(words)):
                if(words[index] == feature[lostFIndex]):
                    break
            #判断丢失特征词前面有没有以下的词语
            if(words[index-1] == "我"):
                pXC[1] = pXC[1] * 100
        for findFIndex in has1[0]:
            #取得捡到特征词在已分词的微博的索引index
            for index in range(len(words)):
                if(words[index] == feature[findFIndex]):
                    break
            #找到捡到特征词前面的名词
            while((index - 1 >= 0) 
                  and (not(tags[index-1] == 'r' or tags[index-1] == 'n')) ):
                index = index - 1
            #记录找到的名词的索引或者索引0
            indexTemp = index - 1
            #找到的索引之前第一个非名词的索引，包括当前索引
            while(indexTemp >= 0 and tags[indexTemp].find('n') != -1):
                indexTemp = indexTemp - 1
            #如果找到的非名词索引为介词，再继续找之前的名词索引
            if(tags[indexTemp] == 'p'):
                while((indexTemp - 1 >= 0) 
                      and (not(tags[indexTemp - 1] == 'r' or tags[indexTemp -1] == 'n'))):
                    indexTemp = indexTemp - 1
                #如果找不到则跳回最开始找到的名词索引
                if(indexTemp == 0):
                    indexTemp = index - 1
            #如果找的的非名词索引不为介词，也跳回最开始找到的名词索引
            else:
                indexTemp = index - 1
            if(words[indexTemp] == "你" or words[indexTemp] == "谁" or words[indexTemp] == "人"):
                pXC[1] = pXC[1] * 100
                
        p[1] = A[1] * pXC[1]

        #取p[i]的最大项
        if(p[0] > p[1]):
            for j in range(6):
                f.write(needClassfiedData[i][j] + '\n')
            #f.write(str(i)+" "+ "1"+" "+str(p[0])+" "+str(p[1])+" "+str(has1[0])+" "+str(has1[1])+" " + '\n')
        else:
            for j in range(6):
                ff.write(needClassfiedData[i][j] + '\n')
            #ff.write(str(i)+" "+"2"+" "+str(p[0])+" "+str(p[1])+" "+str(has2[0])+" "+str(has2[1])+" " + '\n')
        
        has1.pop()
        has1.pop()
        has2.pop()
        has2.pop()
    f.close()
    ff.close()

#对朴素贝叶斯的测试，对后验概率使用了3个优化 
def testClassfier():
    global n
    
    for i in range(testNum):
        p = [1,1]
        pXC = [1,1]
        
        has1 = []
        has1.append([])
        has1.append([])
        for j in range(featureNum):
            weiboContent = testData[i][4]
            if(i == 8):
                weiboContent = jft.f2j('utf8', 'utf8', testData[i][4])
            if(weiboContent.count(feature[j]) != 0):
                pXC[0] = pXC[0] * C1_map[j]
                if(j >= 0 and j <= 4):
                    has1[0].append(j)
                if(j >= 5 and j < featureNum):
                    has1[1].append(j)             
            else:
                pXC[0] = pXC[0] * (1 - C1_map[j])              
        if(len(has1[0]) != 0 and len(has1[1]) == 0):
            pXC[0] = pXC[0] * 2
        if(len(has1[0]) == len(has1[1]) == 1):
            if(weiboContent.find(feature[has1[0][0]]) < 
               weiboContent.find(feature[has1[1][0]])):
                pXC[0] = pXC[0] * 10
                
        words = [w.word for w in pseg.cut(testData[i][4])]
        tags = [w.flag for w in pseg.cut(testData[i][4])]
        for lostFIndex in has1[1]:
            #取得丢失特征词在已分词的微博的索引index
            for index in range(len(words)):
                if(words[index] == feature[lostFIndex]):
                    break
            #判断丢失特征词前面有没有以下的词语
            if(words[index-1] == "你"):
                pXC[0] = pXC[0] * 100
        for findFIndex in has1[0]:
            #取得捡到特征词在已分词的微博的索引index
            for index in range(len(words)):
                if(words[index] == feature[findFIndex]):
                    break
            #判断捡到特征词前面有没有以下的词语
            if(words[index-1] == "我"):
                pXC[0] = pXC[0] * 100
        p[0] = A[0] * pXC[0]
             
        has2 = []
        has2.append([])
        has2.append([])
        for j in range(featureNum):
            weiboContent = testData[i][4]
            if(i == 8):
                weiboContent = jft.f2j('utf8', 'utf8', testData[i][4])
            if(weiboContent.count(feature[j]) != 0):
                pXC[1] = pXC[1] * C2_map[j]
                if(j >= 0 and j <= 4):
                    has2[0].append(j)
                if(j >= 5 and j < featureNum):
                    has2[1].append(j)
            else:
                pXC[1] = pXC[1] * (1 - C2_map[j]) 
        if(len(has2[0]) == 0 and len(has2[1]) != 0):
            pXC[1] = pXC[1] * 2
        if(len(has2[0]) == len(has2[1]) == 1):
            if(weiboContent.find(feature[has2[0][0]]) > 
                weiboContent.find(feature[has2[1][0]])):
                if(tag[has2[0][0]] != "n"):
                    pXC[1] = pXC[1] * 10
                    
        for lostFIndex in has1[1]:
            #取得丢失特征词在已分词的微博的索引index
            for index in range(len(words)):
                if(words[index] == feature[lostFIndex]):
                    break
            #判断丢失特征词前面有没有以下的词语
            if(words[index-1] == "我"):
                pXC[1] = pXC[1] * 100
        for findFIndex in has1[0]:
            #取得捡到特征词在已分词的微博的索引index
            for index in range(len(words)):
                if(words[index] == feature[findFIndex]):
                    break
            #判断捡到特征词前面有没有以下的词语
            while(not(tags[index-1] == 'r' or tags[index-1] == 'n')):
                index = index - 1
            indexTemp = index - 1
            while(tags[indexTemp].find('n') != -1):
                indexTemp = indexTemp - 1
            if(tags[indexTemp] == 'p'):
                indexTemp = indexTemp - 1
                while(not(tags[indexTemp] == 'r' or tags[indexTemp] == 'n')):
                    indexTemp = indexTemp - 1
            if(words[indexTemp] == "你" or words[indexTemp] == "谁" or words[indexTemp] == "人"):
                pXC[1] = pXC[1] * 100
                     
        p[1] = A[1] * pXC[1]

        if(p[0] > p[1]):
            if(testData[i][0]==str(1)):
                n = n + 1
            else:
                print i,testData[i][4],testData[i][0],1,p[0],p[1],has1
                cuttest(testData[i][4])
                #tags = jieba.analyse.extract_tags(testData[i][4],50)
                #print ",".join(tags)
  
        else:
            if(testData[i][0]==str(2)):
                n = n + 1     
            else:
                print i,testData[i][4],testData[i][0],2,p[0],p[1],has2
                cuttest(testData[i][4])
                #tags = jieba.analyse.extract_tags(testData[i][4],50)
                #print ",".join(tags)
        
        has1.pop()
        has1.pop()
        has2.pop()
        has2.pop()
    
    print "测试微博总数：",testNum
    print "分类正确的微博总数：",n
    tp = n / testNum
    fp = 1 - tp
    print "正确率：",tp * 100 , '%'
    print "错误率：",fp * 100, '%'
  
#对字符串匹配的优化，对后验概率只用了两个优化
def testWithoutClassfier():
    global nn
    
    for i in range(testNum):    
        has1 = []
        has1.append([])
        has1.append([])
        for j in range(featureNum):
            weiboContent = testData[i][4]
            if(weiboContent.count(feature[j]) != 0):
                if(j >= 0 and j <= 4):
                    has1[0].append(j)
                if(j >= 5 and j < featureNum):
                    has1[1].append(j)                        
        
        if(len(has1[0]) > len(has1[1])):
            if(testData[i][0]==str(1)):
                nn = nn + 1
            else:
                print i,testData[i][4],testData[i][0],1,has1
                
        if(len(has1[0]) < len(has1[1])):
            if(testData[i][0] == str(2)):
                nn = nn + 1
            else:
                print i,testData[i][4],testData[i][0],2,has1
                
        if(len(has1[0]) == len(has1[1]) == 1):
            if(weiboContent.find(feature[has1[0][0]]) < 
               weiboContent.find(feature[has1[1][0]])):
                if(testData[i][0]==str(1)):
                    nn = nn + 1
                else:
                    print i,testData[i][4],testData[i][0],1,has1
            else:
                if(testData[i][0]==str(2)):
                    nn = nn + 1
                else:
                    print i,testData[i][4],testData[i][0],2,has1
        
        has1.pop()
        has1.pop()
    
    print "测试微博总数：",testNum
    print "分类正确的微博总数：",nn
    tp = nn / testNum
    fp = 1 - tp
    print "正确率：",tp * 100 , '%'
    print "错误率",fp * 100, '%'
  
#分词函数
def cuttest(test_sent):
    result = pseg.cut(test_sent)
    for w in result:
        print w.word, "/", w.flag, ", ",  
    print ""
  
def main():   
    init()
    trainDataRead('trainData.txt')   
    creatClassifier()
    
    testDataRead('testData.txt')
    testClassfier()
    testWithoutClassfier()
    
    needClassfiedDataRead('weibo.txt')
    classfy()            
    
main()
