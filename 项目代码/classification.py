# -*- coding: utf-8 -*-

#search函数，参数为输入文件，输出文件，关键词。关键词与输入文件的每六行进行匹配（六行为一条微博），如果出现该关键词，则把该微博输出到输出文件中
def search(input_file,output_file,key):
    
    line = input_file.readline()
    if line == "\n":
        line = input_file.readline()
    
    while line: #如果文件没有结束，继续读取
        lines = ""
        lines += line
		
        for i in range (1,6):
            line = input_file.readline()
            lines += line #在文件中连续读六行，并放到lines中
        
        index = lines.find(key)
        if index == -1:  #如果找不到关键词，pass
            pass
        else:
            output_file.write(lines) #若找到，则写到输出文件中
            
        line = input_file.readline()
		
try:
    s = "\n"     
    inputFile=open("data/weibo.txt","r")  #在所有微博中匹配关键词
    wallet=open("data/allClasses/wallet.txt","w")
    wallet.write(s)
    search(inputFile,wallet,"钱包") #匹配关键词“钱包”
    inputFile.close()
    wallet.close()
    
    inputFile=open("data/weibo.txt","r")
    campuscard=open("data/allClasses/campuscard.txt","w")
    campuscard.write(s)
    search(inputFile,campuscard,"校园卡") #匹配关键词“校园卡”
    inputFile.close()
    campuscard.close()
    
    inputFile=open("data/weibo.txt","r")
    bankcard=open("data/allClasses/bankcard.txt","w")
    bankcard.write(s)
    search(inputFile,bankcard,"银行卡") #匹配关键词“银行卡”
    inputFile.close()
    bankcard.close()

    inputFile=open("data/weibo.txt","r")
    idcard=open("data/allClasses/IDcard.txt","w")
    idcard.write(s)
    search(inputFile,idcard,"身份证") #匹配关键词“身份证”
    inputFile.close()
    idcard.close()

    inputFile=open("data/weibo.txt","r")
    cellphone=open("data/allClasses/cellphone.txt","a")
    cellphone.truncate()
    cellphone.write(s)
    search(inputFile,cellphone,"手机") #匹配关键词“手机”
    inputFile.close()
    cellphone.close()

    inputFile=open("data/weibo.txt","r")
    cellphone=open("data/allClasses/cellphone.txt","a")
    search(inputFile,cellphone,"iphone")
    inputFile.close()
    cellphone.close()

    inputFile=open("data/weibo.txt","r")
    key=open("data/allClasses/key.txt","w")
    key.write(s)
    search(inputFile,key,"钥匙") #匹配关键词“钥匙”
    inputFile.close()
    key.close()

    inputFile=open("data/weibo.txt","r")
    flashdisk=open("data/allClasses/flashdisk.txt","a")
    flashdisk.truncate()
    flashdisk.write(s)
    search(inputFile,flashdisk,"U盘") #匹配关键词“U盘”
    inputFile.close()
    flashdisk.close()

    inputFile=open("data/weibo.txt","r")
    flashdisk=open("data/allClasses/flashdisk.txt","a")
    search(inputFile,flashdisk,"优盘")
    inputFile.close()
    flashdisk.close()

    

except IOError,e:     
    print "open file error",e


try:
    inputFile=open("data/find.txt","r")  #在“找到”的微博中匹配关键词
    wallet=open("data/findClasses/wallet.txt","w")
    search(inputFile,wallet,"钱包")
    inputFile.close()
    wallet.close()
    
    inputFile=open("data/find.txt","r")
    campuscard=open("data/findClasses/campuscard.txt","w")
    search(inputFile,campuscard,"校园卡")
    inputFile.close()
    campuscard.close()
    
    inputFile=open("data/find.txt","r")
    bankcard=open("data/findClasses/bankcard.txt","w")
    search(inputFile,bankcard,"银行卡")
    inputFile.close()
    bankcard.close()

    inputFile=open("data/find.txt","r")
    idcard=open("data/findClasses/IDcard.txt","w")
    search(inputFile,idcard,"身份证")
    inputFile.close()
    idcard.close()

    inputFile=open("data/find.txt","r")
    cellphone=open("data/findClasses/cellphone.txt","a")
    cellphone.truncate()
    search(inputFile,cellphone,"手机")
    inputFile.close()
    cellphone.close()

    inputFile=open("data/find.txt","r")
    cellphone=open("data/findClasses/cellphone.txt","a")
    search(inputFile,cellphone,"iphone")
    inputFile.close()
    cellphone.close()

    inputFile=open("data/find.txt","r")
    key=open("data/findClasses/key.txt","w")
    search(inputFile,key,"钥匙")
    inputFile.close()
    key.close()

    inputFile=open("data/find.txt","r")
    flashdisk=open("data/findClasses/flashdisk.txt","a")
    flashdisk.truncate()
    search(inputFile,flashdisk,"U盘")
    inputFile.close()
    flashdisk.close()

    inputFile=open("data/find.txt","r")
    flashdisk=open("data/findClasses/flashdisk.txt","a")
    search(inputFile,flashdisk,"优盘")
    inputFile.close()
    flashdisk.close()

    

except IOError,e:     
    print "open file error",e


try:

    inputFile=open("data/lost.txt","r")  #在“丢失”的微博中匹配关键词
    wallet=open("data/lostClasses/wallet.txt","w")
    search(inputFile,wallet,"钱包")
    inputFile.close()
    wallet.close()
    
    inputFile=open("data/lost.txt","r")
    campuscard=open("data/lostClasses/campuscard.txt","w")
    search(inputFile,campuscard,"校园卡")
    inputFile.close()
    campuscard.close()
    
    inputFile=open("data/lost.txt","r")
    bankcard=open("data/lostClasses/bankcard.txt","w")
    search(inputFile,bankcard,"银行卡")
    inputFile.close()
    bankcard.close()

    inputFile=open("data/lost.txt","r")
    idcard=open("data/lostClasses/IDcard.txt","w")
    search(inputFile,idcard,"身份证")
    inputFile.close()
    idcard.close()

    inputFile=open("data/lost.txt","r")
    cellphone=open("data/lostClasses/cellphone.txt","a")
    cellphone.truncate()
    search(inputFile,cellphone,"手机")
    inputFile.close()
    cellphone.close()

    inputFile=open("data/lost.txt","r")
    cellphone=open("data/lostClasses/cellphone.txt","a")
    search(inputFile,cellphone,"iphone")
    inputFile.close()
    cellphone.close()

    inputFile=open("data/lost.txt","r")
    key=open("data/lostClasses/key.txt","w")
    search(inputFile,key,"钥匙")
    inputFile.close()
    key.close()

    inputFile=open("data/lost.txt","r")
    flashdisk=open("data/lostClasses/flashdisk.txt","a")
    flashdisk.truncate()
    search(inputFile,flashdisk,"U盘")
    inputFile.close()
    flashdisk.close()

    inputFile=open("data/lost.txt","r")
    flashdisk=open("data/lostClasses/flashdisk.txt","a")
    search(inputFile,flashdisk,"优盘")
    inputFile.close()
    flashdisk.close()

    

except IOError,e:     
    print "open file error",e
    
