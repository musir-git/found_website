# -*- coding: utf-8 -*-
from __future__ import division
import codecs

trainData = []
testData = []
needClassfiedData = []
trainNum = 0
testNum = 0
needClassfiedNum = 0 
C1_map = []
C2_map = []
feature = ["捡","拾","失主","认领","拣","丢","遗","落","掉","忘","不见","望","求","麻烦","谢","感激"]
featureNum = len(feature)

A=[0,0]
n = 0
nn = 0

def init():
    for i in range(featureNum):
        C1_map.append(0)
    for i in range(featureNum):
        C2_map.append(0)

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
    
def creatClassifier():
    global trainNum
    count1 = 0
    count2 = 0
    
    for i in range(trainNum):
        if(trainData[i][0] == str(1)):
            count1 = count1 + 1
        if(trainData[i][0] == str(2)):
            count2 = count2 + 1
            
    A[0] = count1/trainNum
    A[1] = count2/trainNum

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

    for i in range(featureNum):
        #if(C1_map[i] == 0):
        #    C1_map[i] = 1
        #C1_map[i] = C1_map[i]/count1
        C1_map[i] = (C1_map[i] + 1)/count1
        #if(C2_map[i] == 0):
        #    C2_map[i] = 1
        #C2_map[i] = C2_map[i]/count1  
        C2_map[i] = (C2_map[i] + 1)/count2

def classfy():
    f = open("data/find.txt", 'w+')
    ff = open("data/lost.txt", 'w+')
    for i in range(needClassfiedNum):
        p = [1,1]
        pXC = [1,1]
        
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
        if(len(has1[0]) != 0 and len(has1[1]) == 0):
            pXC[0] = pXC[0] * 2
        if(len(has1[0]) == len(has1[1]) == 1):
            if(weiboContent.find(feature[has1[0][0]]) < 
               weiboContent.find(feature[has1[1][0]])):
                pXC[0] = pXC[0] * 10
        p[0] = A[0] * pXC[0]
        
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
        if(len(has2[0]) == 0 and len(has2[1]) != 0):
            pXC[1] = pXC[1] * 2
        if(len(has2[0]) == len(has2[1]) == 1):
            if(weiboContent.find(feature[has2[0][0]]) > 
               weiboContent.find(feature[has2[1][0]])):
                pXC[1] = pXC[1] * 10
        p[1] = A[1] * pXC[1]

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
        p[0] = A[0] * pXC[0]
        
        has2 = []
        has2.append([])
        has2.append([])
        for j in range(featureNum):
            weiboContent = testData[i][4]
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
                pXC[1] = pXC[1] * 10
        p[1] = A[1] * pXC[1]

        if(p[0] > p[1]):
            if(testData[i][0]==str(1)):
                n = n + 1
            else:
                print i,testData[i][4],testData[i][0],1,p[0],p[1],has1
  
        else:
            if(testData[i][0]==str(2)):
                n = n + 1     
            else:
                print i,testData[i][4],testData[i][0],2,p[0],p[1],has2
        
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
    tp = n / testNum
    fp = 1 - tp
    print "正确率：",tp * 100 , '%'
    print "错误率",fp * 100, '%'
    
def main():   
    init()
    trainDataRead('data/trainData.txt')   
    creatClassifier()
    
    #testDataRead('data/testData.txt')
    #testClassfier()
    #testWithoutClassfier()
    
    needClassfiedDataRead('data/weibo.txt')
    classfy()

main()
