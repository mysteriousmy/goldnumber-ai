from pyswagger import App
from pyswagger.contrib.client.requests import Client

import random
import time
import os
import argparse
import numpy as np
import pandas as pd

class QLTable:
    def __init__(self, actions, learning_rate = 0.1, reward_decay = 0.9, greedy = 0.9, up = 0, down = 0):
        self.actions = actions # 执行的算法
        self.lr = learning_rate # 学习率
        self.gamma = reward_decay #奖励衰变值
        self.greedy = greedy #贪心算法中的贪心率
        self.q_table = pd.DataFrame(columns = self.actions, dtype = np.float64)
        self.up = up #此轮前十个黄金点的上界
        self.down = down #此轮前十个黄金点的下界
        #下面分为几个函数来影响到qtable 决定程序的策略
        #检查state是否存在
    def check_state(self, state):
        #如果一个state不存在于table里则创建并初始化列值
        print(self.q_table)
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                #根据提供的action数量来初始化第二列值
                pd.Series(
                    [0]  * len(self.actions),
                    index = self.q_table.columns,
                    name = state
                )
            )
    def choose_action(self, state):
        #先检查状态是否存在于qtable 不存在则创建一列
        self.check_state(state)
        #如果np随机生成的[0-1)的浮点数小于贪心率或者大于执行的action
        if np.random.uniform() < self.greedy:
            #设定一个最佳选择的列state_action为 state + 后面的算法序列
            state_action = self.q_table.loc[state, :]
            #在列中相同期望值里所有最大的action中，利用np随机抽取算法action，
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        else:
            #大于贪心率 则将action一直取前面的actions ？？？？？？
            action = np.random.choice(self.actions)
        return action
    #下面为学习更新qtable
    def learn(self, ls, la, lr , s):
        self.check_state(s)
        #这里解释下参数
        '''
            ls是前一次状态列，la是前一次的action，lr是前一次得到的分数，s是当前黄金点计算的state
        '''
        #定义一个预测的qtable q_predict为修改前一次状态列的action
        q_predict = self.q_table.loc[ls, la]
        #s 不为terminal（其实开始第二轮咋都不会等于这个值啊）
        if s != 'terminal':
            #定义修改目标值为前一轮得分+γ* qtable当前取的状态列中的最大值
            #对应公式的部分R + γmaxQ（S‘，a）
            q_target = lr + self.gamma * self.q_table.loc[s, :].max()
        else:
            #如果为terminal 初始化q_target为前一轮分数
            q_target = lr
        #开始更新qtable，此处对应完整qlearning更新公式
        self.q_table.loc[ls, la] += self.lr * (q_target - q_predict)
    #取得状态行
    def getState(self,goldenNumberList):
        # 如果历史黄金点为0 - 1 ，不大于1 则创建0_0状态
        if len(goldenNumberList) == 0 or len(goldenNumberList) == 1:
            return '0_0'
        else:
            #否则先用np.array将历史小于等于10个的黄金点转换成array
            sub = np.array(goldenNumberList[-10:])
            #定义sub1 为下标0-9的历史黄金点
            sub1 = sub[:-1]
            #定义sub2 为下标1-10的历史黄金点
            sub2 = sub[1:]
            #两个array相减
            diff = sub1 - sub2
            #下面为计算前十轮的黄金点状态的最低下界和最高上界 整数型
            self.up = sum(1 for e in diff if e < 0 )
            #这个方法有必要解释下，意思是迭代array每个符合条件的数字，并给他们都+1，然后再sum下，就得出来了
            self.down = sum(1 for e in diff if e > 0)
            #返回状态名
            return '{}_{}'.format(self.up, self.down)
    def cleanAll(self):
        self.actions = 0 # 执行的算法
        self.lr = 0.1 # 学习率
        self.gamma = 0.9 #奖励衰变值
        self.greedy = 0.9 #贪心算法中的贪心率
        self.q_table = pd.DataFrame()
        self.up = 0 #此轮前十个黄金点的上界
        self.down = 0 #此轮前十个黄金点的下界
class Action:
    def __init__(self, goldenNumberList,number):
        self.goldenNumberList = goldenNumberList
        self.number = number

    def doAction(self,  actions):
        if actions == 0:
            number = self.number
            if len(self.goldenNumberList) != 0:
                number = self.goldenNumberList[-1]
            return number, number
        elif actions == 1:
            number = self.number
            if len(self.goldenNumberList) != 0:
                number = self.goldenNumberList[-1]*0.618
            return number, number
        elif actions == 2:
            number = self.number
            if len(self.goldenNumberList) != 0:
                number = np.average(self.goldenNumberList[-5:])
            return number, number
        elif actions == 3:
            number = self.number
            if len(self.goldenNumberList) != 0:
                number = np.average(self.goldenNumberList[-5:])*0.618
            return number, number
        elif actions == 4:
            number = self.number
            if len(self.goldenNumberList) != 0:
                number = np.average(self.goldenNumberList[-10:])
            return number, number
        elif actions == 5:
            number = self.number
            if len(self.goldenNumberList) != 0:
                number = np.average(self.goldenNumberList[-10:])*0.618
            return number, number
        elif actions == 6:
            if len(self.goldenNumberList) == 0:
                return 28, 28
            if len(self.goldenNumberList) == 1:
                return self.goldenNumberList[0], self.goldenNumberList[0]
            number = self.goldenNumberList[-1] / self.goldenNumberList[-2] * self.goldenNumberList[-1]
            if number <= 0:
                number = 0.001
            if number >= 100:
                number = 100*0.618
            return number, number
        else:
            return 0,0

lastState = None
lastAction = None
RL = QLTable(actions=list(range(7)))

def GeneratePredictionNumbers(goldenNumberList, lastScore, numberCount):
    global lastState
    global lastAction
    AC = Action(goldenNumberList=goldenNumberList, number=28)
    
    state = RL.getState(goldenNumberList)
    
    if lastState != None and lastAction != None:
        RL.learn(lastState, lastAction, lastScore, state)
    action = RL.choose_action(state)
    
    number1, number2 = AC.doAction(action)
    
    lastState = state
    lastAction = action
    
    return number1, number2

class gogogo:
    def __init__(self, host, jsonpath, roomId):
        self.host = host
        self.jsonpath = jsonpath
        self.roomId = roomId
        self.__app = App._create_(self.host + self.jsonpath)
        self.__client = Client()
    # def setServer(self):
    #     app
    def start(self):
        user, userId = self.__InitConfigrue()
        self.__Submit(user, userId, self.roomId)
    def __InitConfigrue(self):
        if self.roomId is None:
            self.roomId = input("输入房间号：")
            try:
                self.roomId = int(self.roomId)
            except:
                self.roomId = 0
                print('你tm乱输入啥呢，给爷去0号玩泥巴吧')
        userInfoFile = "userinfo.txt"
        userId = None
        nickName = None
        user = None
        try:
            with open(userInfoFile) as f:
                userId, nickName = f.read().split(',')[:2]
            print('使用本地存储玩家：' + nickName + ' Uid:' + userId)
        except:
            userResp = self.__client.request(
                self.__app.op['NewUser'](
                    nickName = '楠哥无敌队'
                )
            )
            assert userResp.status == 200
            user = userResp.data
            userId = user.userId
            nickName = user.nickName
            print('创建一个新的玩家： ' + nickName + 'Uid：' + userId)
            with open(userInfoFile, 'w') as f:
                f.write("%s,%s" % (userId, nickName))
        print('当前房间号：' + str(self.roomId))
        return user, userId

    def __Submit(self, user, userId, roomId):
        while True:
            stateResp = self.__client.request(
                self.__app.op['State'](
                    uid = userId,
                    roomid = roomId
                )
            )
            if stateResp.status != 200:
                print('网络炸了，自己看着办')
                time.sleep(1)
                continue
            state = stateResp.data

            if state.state == 2:
                print('游戏结束，洗洗睡吧，修仙的')
                break

            if state.state == 1:
                print('服务器没开游戏，自己看着办,要不你去揍运维？')
                time.sleep(1)
                continue

            if state.hasSubmitted:
                print('准备下一回合的扣分，怕不怕?')
                if state.maxUserCount == 0:
                    time.sleep(state.leftTime + 1)
                else:
                    time.sleep(1)
                continue

            todayGoldenListResp = self.__client.request(
                self.__app.op['TodayGoldenList'](
                    roomid = roomId
                )
            )
            if todayGoldenListResp.status != 200:
                print('你网络又炸了，自己看着办')
                time.sleep(1)
                continue
            todayGoldenList = todayGoldenListResp.data
            if len(todayGoldenList.goldenNumberList) != 0:
                print('上一轮的黄金点是: ' + str(todayGoldenList.goldenNumberList[-1]))

            lastRoundResp = self.__client.request(
                self.__app.op['History'](
                    roomid = roomId,
                    count = 1
                )
            )
            if lastRoundResp.status != 200:
                print('你网络又又又炸了，自己看着办')
                time.sleep(1)
                continue
            lastScore = 0
            if len(lastRoundResp.data.rounds) > 0:
                scoreArray = [user for user in lastRoundResp.data.rounds[0].userNumbers if user.userId == userId]
                if len(scoreArray) == 1:
                    lastScore = scoreArray[0].score
            print('上一轮的得分是：{}'.format(lastScore))

            number1, number2 = GeneratePredictionNumbers(todayGoldenList.goldenNumberList, lastScore, state.numbers)
            if(state.numbers == 2):
                submitRsp = self.__client.request(
                    self.__app.op['Submit'](
                        uid = userId,
                        rid = state.roundId,
                        n1 = str(number1),
                        n2 = str(number2)
                    )
                )
                if submitRsp.status == 200:
                    print('你瞎猜的两个数字是：' + str(number1) + ', ' + str(number2))
                else:
                    print('哥哥你的bot智障拉：' + submitRsp.data.message)
                    time.sleep(1)
            else:
                submitRsp = self.__client.request(
                    self.__app.op['Submit'](
                        uid = userId,
                        rid = state.roundId,
                        n1 = str(number1)
                    )
                )
                print(submitRsp.status)
                if submitRsp.status == 200:
                    print('你瞎猜的数字是：' + str(number1))
                else:
                    print('骚年，你哪又搞出exception了？' + submitRsp.data.message)
                    if(submitRsp.data.message == 'Invalid uid'):
                        os.remove("userInfo.txt")
                        self.__InitConfigrue()
                        RL.cleanAll()
                        continue
                    time.sleep(1)

def main(roomId):
    go = gogogo("https://goldennumber.aiedu.msra.cn/", "/swagger/v1/swagger.json", None)
    go.start()
# host = 'https://goldennumber.aiedu.msra.cn/'
# jsonpath = '/swagger/v1/swagger.json'
# app = App._create_(host + jsonpath)
# client = Client()

# def main(roomId):
#     if roomId is None:
#         # Input the roomid if there is no roomid in args
#         roomId = input("Input room id: ")
#         try:
#             roomId = int(roomId)
#         except:
#             roomId = 0
#             print('Parse room id failed, default join in to room 0')

#     userInfoFile = "userinfo.txt"
#     userId = None
#     nickName = None
#     try:
#         # Use an exist player
#         with open(userInfoFile) as f:
#             userId, nickName = f.read().split(',')[:2]
#         print('Use an exist player: ' + nickName + '  Id: ' + userId)
#     except:
#         # Create a new player
#         userResp = client.request(
#             app.op['NewUser'](
#                 nickName='AI Player ' + str(random.randint(0, 9999))
#             ))
#         assert userResp.status == 200
#         user = userResp.data
#         userId = user.userId
#         nickName = user.nickName
#         print('Create a new player: ' + nickName + '  Id: ' + userId)

#         with open(userInfoFile, "w") as f:
#             f.write("%s,%s" % (userId, nickName))

#     print('Room id: ' + str(roomId))

#     while True:
#         stateResp = client.request(
#             app.op['State'](
#                 uid=userId,
#                 roomid=roomId
#             ))
#         if stateResp.status != 200:
#             print('Network issue, query again after 1 second')
#             time.sleep(1)
#             continue
#         state = stateResp.data
    
#         if state.state == 2:
#             print('The game has finished')
#             break

#         if state.state == 1:
#             print('The game has not started, query again after 1 second')
#             time.sleep(1)
#             continue

#         if state.hasSubmitted:
#             print('Already submitted this round, wait for next round')
#             if state.maxUserCount == 0:
#                 time.sleep(state.leftTime + 1)
#             else:
#                 # One round can be finished when all players submitted their numbers if the room have set the max count of users, need to check the state every second.
#                 time.sleep(1)
#             continue

#         print('\r\nThis is round ' + str(state.finishedRoundCount + 1))

#         todayGoldenListResp = client.request(
#             app.op['TodayGoldenList'](
#                 roomid=roomId
#             ))
#         if todayGoldenListResp.status != 200:
#             print('Network issue, query again after 1 second')
#             time.sleep(1)
#             continue
#         todayGoldenList = todayGoldenListResp.data
#         if len(todayGoldenList.goldenNumberList) != 0:
#             print('Last golden number is: ' + str(todayGoldenList.goldenNumberList[-1]))

#         lastRoundResp = client.request(
#             app.op['History'](
#                 roomid=roomId,
#                 count=1
#             ))
#         if lastRoundResp.status != 200:
#             print('Network issue, query again after 1 second')
#             time.sleep(1)
#             continue
#         lastScore = 0
#         if len(lastRoundResp.data.rounds) > 0:
#             scoreArray = [user for user in lastRoundResp.data.rounds[0].userNumbers if user.userId == userId]
#             if len(scoreArray) == 1:
#                 lastScore = scoreArray[0].score
#         print('Last round score: {}'.format(lastScore))

#         number1, number2 = GeneratePredictionNumbers(todayGoldenList.goldenNumberList, lastScore, state.numbers)

#         if (state.numbers == 2):
#             submitRsp = client.request(
#                 app.op['Submit'](
#                     uid=userId,
#                     rid=state.roundId,
#                     n1=str(number1),
#                     n2=str(number2)
#                 ))
#             if submitRsp.status == 200:
#                 print('You submit numbers: ' + str(number1) + ', ' + str(number2))
#             else:
#                 print('Error: ' + submitRsp.data.message)
#                 time.sleep(1)

#         else:
#             submitRsp = client.request(
#                 app.op['Submit'](
#                     uid=userId,
#                     rid=state.roundId,
#                     n1=str(number1)
#                 ))
#             if submitRsp.status == 200:
#                 print('You submit number: ' + str(number1))
#             else:
#                 print('Error: ' + submitRsp.data.message)
#                 time.sleep(1)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--room', type=int, help='Room ID', required=False)
    args = parser.parse_args()

    main(args.room)