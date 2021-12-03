import package.doaction as do
import package.QLCore as ql
import package.networkApi as gos
import os
import random
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
RL = ql.QLTable(actions=list(range(len(caculateAl()))), isUseLocalQLTable=True)
RL.checkLocalQTable()

#Action类，做些无聊的事，可能是瞎猜，可能是楠哥无敌卡尔曼滤波流
#numbers觉得碍眼, 已经被我灭掉
class Action:
    def __init__(self, goldenNumberList):
        self.goldenNumberList = goldenNumberList
        self.__d = caculateAl()
    #根据反馈的状态和人工智障认为要瞎猜的步骤来调用对应的算法
    def doAction(self,  actions):
        pyfile = self.__d[actions]
        print(self.__d)
        print('选择算法：%s' % actions)
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

def angel(v1, v2):
    x = np.array([1, v1])
    y = np.array([1, v2])
    #两个向量
    Lx = np.sqrt(x.dot(x))
    Ly = np.sqrt(y.dot(y))
    #相当于勾股定理
    cos_angle = x.dot(y) / (Lx * Ly)
    #求得cos_sita的值再反过来计计算绝对值
    print(cos_angle)
    angle = np.arccos(cos_angle)
    angle2 = angle * 360 / 2 / np.pi
    return angle2
#生成预测数
def GeneratePredictionNumbers(goldenNumberList, lastScore, numberCount):
    global lastState
    global lastAction
    number1 = 0
    number2 = 0
    if len(goldenNumberList) == 0:
        number1 = random.uniform(1,50)
        number2 = random.uniform(1,50)
    else:
        AC = Action(goldenNumberList=goldenNumberList)

        state = RL.getState(goldenNumberList)

        if lastState != None and lastAction != None:
            RL.learn(lastState, lastAction, lastScore, state)
        action = RL.choose_action(state)
        number1, number2 = AC.doAction(action)
        if len(goldenNumberList) >= 4:
            v1 = abs(goldenNumberList[-1]- goldenNumberList[-2])
            v2 = abs(goldenNumberList[-3]-goldenNumberList[-4])
            if angel(v1, v2) <= 10:
                number1 = goldenNumberList[-1]
                number2 = goldenNumberList[-2]
        lastState = state
        lastAction = action

    return number1, number2


