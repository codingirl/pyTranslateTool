# -*- coding:utf-8 -*-
# pyTranslateTool
"""
A small translation tool that I wrote just for fun.
You can configure a quick command in bush
So when you translate something,you can do it more quickly and easily.
"""
import requests
import json

class Fanyi:
    def __init__(self):
        self.langdetectUrl='http://fanyi.baidu.com/langdetect'
        self.post_url="http://fanyi.baidu.com/v2transapi"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
        self.langsDict = {"zh":"汉语", "en": "英语", "ru":"俄语", "fra": "法语","kor":"韩语"}
        self.__query_string=''
        self.__lanDectParam=''
        self.__postData=''
        self.__loop=True

    @property
    def loop(self):
        return self.__loop

    @loop.setter
    def loop(self,value):
        self.__loop=value

    @property
    def query_string(self):
        return self.__query_string

    @query_string.setter
    def query_string(self, value):
        self.__query_string = value

    @property
    def lanDectParam(self):
        return  self.__lanDectParam

    @lanDectParam.setter
    def lanDectParam(self,value):
        self.__lanDectParam={"query": value}

    @property
    def postData(self):
        return self.__postData

    @postData.setter
    def postData(self,value):
        self.__postData={
            "from":value[0],
            "to": value[1],
            "query": value[2],
            "transtype": "realtime",
            "simple_means_flag": "3"
        }


    def param_url(self):
        req = requests.post(self.post_url, data=self.postData, headers=self.header)
        r=req.content.decode()
        return r

    def getResult(self,req):
        dict_response = json.loads(req)
        ret =dict_response["trans_result"]["data"][0]["dst"]
        return ret

    def getFromLan(self):
        req = requests.post(self.langdetectUrl, data=self.lanDectParam, headers=self.header)
        r = req.content.decode()
        # print(r)
        dictObj=json.loads(r)
        return dictObj['lan']


    def step1_getFromLan(self):
        # 1. 自动检测输入的语言类型
        queryKeyWord = input('请输入您要翻译的词汇：')
        if queryKeyWord=='stop':
            self.loop=False
            return ''
        self.query_string = queryKeyWord
        self.lanDectParam = queryKeyWord
        fLanRet = self.getFromLan()
        hanyuFromLan = self.langsDict[fLanRet]
        print('检测到您输入的为' + hanyuFromLan)
        return fLanRet

    def step2_getDstLan(self):
        # 2.选择翻译语言类型
        if self.loop==False:
            return ''
        print('您想要翻译成下列哪种语言? ')
        for i in fanyi.langsDict.keys():
            print(i + ' -- ' + fanyi.langsDict[i])
        print('请输入语言缩略字母：')
        dstLan = input()
        return dstLan

    def step3_getResult(self,value):
        # 3. 翻译..得出翻译结果
        if self.loop==False:
            return
        req = self.param_url()
        result = self.getResult(req)
        print(value[2] + ' 翻译成' + fanyi.langsDict[value[1]] + '是： ', end=result)
        print()

    def run(self):
        while self.loop:
            fLanRet = self.step1_getFromLan()
            dstLan = self.step2_getDstLan()
            value = [fLanRet, dstLan, self.query_string]
            fanyi.postData = value
            self.step3_getResult(value)
            print('----' * 20)
        print('已成功退出xxx翻译小工具')




if __name__ == '__main__':
    fanyi=Fanyi()
    print('****'*10)
    print('欢迎使用xxx翻译小工具。 \n输入stop退出程序')
    print('****' * 10)
    fanyi.run()
