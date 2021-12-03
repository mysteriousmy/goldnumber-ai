import package.doaction as do
import package.QLCore as ql
import package.networkApi as gos
import os
import numpy as np
import pandas as pd

#此部分外面的某些变量纯属懒货写的

#计算引擎（吹牛引擎），计算算法总数和所有算法文件的名字
def caculateAl():
    path = os.path.split(os.path.realpath(__file__))[0] + '\\Algorithm\\'
    d = {}
    filenum = 0
    for lists in os.listdir(path):
        sub_path = os.path.join(path, lists)
        if os.path.isfile(sub_path):
            if os.path.splitext(lists)[1] == '.py' and lists != 'readNum.py':
                d[filenum] = lists
                filenum = filenum + 1
    return d

#上一轮的state和action，至于为什么全局化，天知道
lastState = None
lastAction = None
RL = ql.QLTable(actions=list(range(len(caculateAl()))))

#Action类，做些无聊的事，可能是瞎猜，可能是楠哥无敌卡尔曼滤波流
#numbers觉得碍眼, 已经被我灭掉
class Action:
    def __init__(self, goldenNumberList):
        self.goldenNumberList = goldenNumberList
        self.__d = caculateAl()
    #根据反馈的状态和人工智障认为要瞎猜的步骤来调用对应的算法
    def doAction(self,  actions):
        pyfile = self.__d[actions]
        lists = []
        path = os.path.split(os.path.realpath(__file__))[0]+'\\Algorithm\\' + pyfile
        result = os.popen('python ' + path)
        res = result.read()
        for line in res.splitlines():
            pass
        for i in line.split(','):
            lists.append(float(i))
        number1 = lists[0]
        number2 = lists[1]
        return number1, number2

#生成预测数
def GeneratePredictionNumbers(goldenNumberList, lastScore, numberCount):
    global lastState
    global lastAction
    if len(goldenNumberList) == 0:
        number1,number2 = 28
    else:
        AC = Action(goldenNumberList=goldenNumberList)

        state = RL.getState(goldenNumberList)

        if lastState != None and lastAction != None:
            RL.learn(lastState, lastAction, lastScore, state)
        action = RL.choose_action(state)
        number1, number2 = AC.doAction(action)
        lastState = state
        lastAction = action

    return number1, number2

