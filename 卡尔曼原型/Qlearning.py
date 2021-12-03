import os
from pyswagger import App

from pyswagger.contrib.client.requests import Client

import random

import time

import argparse

# Use `pip install numpy pandas` to install numpy and pandas

import numpy as np

import pandas as pd
import kalman as kalman
class Qlearning():
    def __init__(self, actions, isUseLocalQLTable, greedy=0.7, learning_rate=0.1, reward_decay=0.8 ):
        self.actions = actions
        self.learning_rate = learning_rate
        self.reward_decay = reward_decay
        self.greedy = greedy
        self.q_table = pd.DataFrame(columns = self.actions, dtype = np.float64)
        self.isUseLocalQLTable = isUseLocalQLTable
        pass

    #  检查并追加状态
    def checkISExist(self, state):
        print(self.q_table)
        self.saveQTable()
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index = self.q_table.columns,
                    name = state
                )
            )
        pass

    #  根据状态选择action
    def chooseAction(self, state):
        #  检查这个状态是否存在
        self.checkISExist(state)
        if np.random.uniform() < self.greedy:
            #  小于贪婪度时候选择权值最大action
            state_action = self.q_table.loc[state, :]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
            pass
        else:
            #  随机选择action
            action = np.random.choice((self.actions))
            pass
        return action
        pass

    #  更新qtable
    def learn(self, last_state, last_action, last_reward, state):
        #  检查当前state是否存在
        self.checkISExist(state)
        #  定义预测qtable
        q_predict = self.q_table.loc[last_state, last_action]
        if state != 'terminal':
            q_target = last_reward + self.reward_decay * self.q_table.loc[state, :].max()

            pass
        else:
            q_target = last_reward
            pass
        #  更新qtable
        self.q_table.loc[last_state,last_action] += self.reward_decay*(q_target - q_predict)
        pass
    def checkLocalQTable(self):
        if self.isUseLocalQLTable == True:
            if os.path.exists(r'q_table.xls'):
                self.q_table = pd.read_excel(r'q_table.xls',index_col=0)
            else:
                pass
    def saveQTable(self):
        self.q_table.to_excel(r'q_table.xls',sheet_name="sheet2")
    #  获得所有算法action
    """
    def addAtions(self):
        path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))+ '\\Action\\'
        d = []
        fileNumber = 0
        for lists in os.listdir(path):
            sub_path = os.path.join(path, lists)
            if os.path.isfile(sub_path):
                if os.path.splitext(lists)[1] == '.py':
                    d.append(lists)
                    fileNumber += 1
                    pass
                pass
            pass
        d = list(d)
        l = len(d)
        return d, l
        pass
"""
    def getActions(self):
        return self.allAction
        pass

    #  获得当前状态状态
    def getState(self, goldNumberList):
        if len(goldNumberList) == 0 or len(goldNumberList) == 1:
            return '0_0'
        else:
            sub = np.array(goldNumberList[-10:])

            sub1 = sub[:-1]

            sub2 = sub[1:]

            dif = sub1 - sub2

            up = sum(1 for e in dif if e < 0)

            down = sum(1 for e in dif if e > 0)

            return '{}_{}'.format(up, down)

        pass

        pass

    pass


def action1(gArray):
    number = 28

    if len(gArray) != 0:
        number = gArray[-1]

    number2 = number*0.618

    return number, number2



def action2(goldenNumberList):
    if goldenNumberList[-1] - goldenNumberList[-2] > 0:
        if goldenNumberList[-1] - goldenNumberList[-2] < goldenNumberList[-2] - goldenNumberList[-3]:
            number1 = sum(goldenNumberList[-8:]) / 8 * (0.618 + 1) / 2
    else:
        number1 = (goldenNumberList[-1] - goldenNumberList[-2]) * (0.618 + 1) / 2 + goldenNumberList[-1]
    if goldenNumberList[-1] - goldenNumberList[-2] < 0:
        if goldenNumberList[-2] - goldenNumberList[-1] < goldenNumberList[-3] - goldenNumberList[-2]:
            number1 = sum(goldenNumberList[-8:]) / 8 * (0.618 + 1) / 2
    else:
        number1 = goldenNumberList[-1] - (goldenNumberList[-2] - goldenNumberList[-1]) * (0.618 + 1) / 2
    number2 = number1 * (0.618 + 1) / 2
    return number1, number2


def action3(gArray):
    number = 28

    if len(gArray) != 0:
        number = np.average(gArray[-5:])

    return number, number


def action4(gArray):
    number = 28

    if len(gArray) != 0:
        number = np.average(gArray[-5:]) * 0.618

    return number, number


def action5(gArray):
    #  双重卡尔曼
    number1, number2 = 28,28

    if len(gArray) != 0:
        number1 = np.average(gArray[-2:])*0.618

        number1 = kalman.kalman(gArray, number1)
        number2 = kalman.kalman(gArray, number1)


    return number1, number2


def action6(gArray):
    number = 28

    if len(gArray) != 0:
        number = np.average(gArray[-10:]) * 0.618

    return number, number


def action7(gArray):
    if len(gArray) == 0:
        return 28, 28

    if len(gArray) == 1:
        return gArray[0], gArray[0]

    number = gArray[-1] / gArray[-2] * gArray[-1]

    if number <= 0:
        number = 0.001

    if number >= 100:
        number = 100 * 0.618

    return number, number



actions = []

actions.append(action1)

actions.append(action2)

actions.append(action3)

actions.append(action4)

actions.append(action5)







n_actions = len(actions)

RL = Qlearning(actions=list(range(n_actions)),isUseLocalQLTable=True)
RL.checkLocalQTable()

def getState(gArray):
    if len(gArray) == 0 or len(gArray) == 1:

        return '0_0'

    else:

        sub = np.array(gArray[-10:])

        sub1 = sub[:-1]

        sub2 = sub[1:]

        dif = sub1 - sub2

        up = sum(1 for e in dif if e < 0)

        down = sum(1 for e in dif if e > 0)

        return '{}_{}'.format(up, down)


lastState = None

lastAction = None


def GeneratePredictionNumbers(goldenNumberList, lastScore, numberCount):
    global lastState

    global lastAction

    state = getState(goldenNumberList)

    if lastState != None and lastAction != None:
        RL.learn(lastState, lastAction, lastScore, state)

    action = RL.chooseAction(state)

    number1, number2 = actions[action](goldenNumberList)

    lastState = state

    lastAction = action
    #  过滤器

    #  求两向量夹角，小于15，则认为是平滑曲线
    if len(goldenNumberList) >= 4:
        v1 = abs(goldenNumberList[-1]- goldenNumberList[-2])
        v2 = abs(goldenNumberList[-3]-goldenNumberList[-4])
        if angle(v1, v2) <= 10:
            number1 = goldenNumberList[-1]
            number2 = goldenNumberList[-2]
            pass
        pass

    #  if abs(abs(goldenNumberList[-1] - goldenNumberList[-2]) - abs(goldenNumberList[-3] - goldenNumberList[-4])) <=











    return number1, number2

def angle(v1, v2):
    x = np.array([1, v1])
    y = np.array([1, v2])
    # 两个向量
    Lx = np.sqrt(x.dot(x))
    Ly = np.sqrt(y.dot(y))
    # 相当于勾股定理，求得斜线的长度
    cos_angle = x.dot(y) / (Lx * Ly)
    # 求得cos_sita的值再反过来计算，绝对长度乘以cos角度为矢量长度，初中知识。。
    print(cos_angle)
    angle = np.arccos(cos_angle)
    angle2 = angle * 360 / 2 / np.pi
    return angle2
    pass

# Init swagger client

host = 'https://goldennumber.aiedu.msra.cn/'

jsonpath = '/swagger/v1/swagger.json'

app = App._create_(host + jsonpath)

client = Client()


def main(roomId):
    if roomId is None:

        # Input the roomid if there is no roomid in args

        roomId = input("Input room id: ")

        try:

            roomId = int(roomId)

        except:

            roomId = 0

            print('Parse room id failed, default join in to room 0')

    userInfoFile = "userinfo.txt"

    userId = None

    nickName = None

    try:

        # Use an exist player

        with open(userInfoFile) as f:

            userId, nickName = f.read().split(',')[:2]

        print('Use an exist player: ' + nickName + '  Id: ' + userId)

    except:

        # Create a new player

        userResp = client.request(

            app.op['NewUser'](

                nickName='我写代码会自闭'

            ))

        assert userResp.status == 200

        user = userResp.data

        userId = user.userId

        nickName = user.nickName

        print('Create a new player: ' + nickName + '  Id: ' + userId)

        with open(userInfoFile, "w") as f:

            f.write("%s,%s" % (userId, nickName))

    print('Room id: ' + str(roomId))

    while True:

        stateResp = client.request(

            app.op['State'](

                uid=userId,

                roomid=roomId

            ))

        if stateResp.status != 200:
            print('Network issue, query again after 1 second')

            time.sleep(1)

            continue

        state = stateResp.data

        if state.state == 2:
            print('The game has finished')

            break

        if state.state == 1:
            print('The game has not started, query again after 1 second')

            time.sleep(1)

            continue

        if state.hasSubmitted:

            print('Already submitted this round, wait for next round')

            if state.maxUserCount == 0:

                time.sleep(state.leftTime + 1)

            else:

                # One round can be finished when all players submitted their numbers if the room have set the max count of users, need to check the state every second.

                time.sleep(1)

            continue

        print('\r\nThis is round ' + str(state.finishedRoundCount + 1))

        todayGoldenListResp = client.request(

            app.op['TodayGoldenList'](

                roomid=roomId

            ))

        if todayGoldenListResp.status != 200:
            print('Network issue, query again after 1 second')

            time.sleep(1)

            continue

        todayGoldenList = todayGoldenListResp.data

        if len(todayGoldenList.goldenNumberList) != 0:
            print('Last golden number is: ' + str(todayGoldenList.goldenNumberList[-1]))

        lastRoundResp = client.request(

            app.op['History'](

                roomid=roomId,

                count=1

            ))

        if lastRoundResp.status != 200:
            print('Network issue, query again after 1 second')

            time.sleep(1)

            continue

        lastScore = 0

        if len(lastRoundResp.data.rounds) > 0:

            scoreArray = [user for user in lastRoundResp.data.rounds[0].userNumbers if user.userId == userId]

            if len(scoreArray) == 1:
                lastScore = scoreArray[0].score

        print('Last round score: {}'.format(lastScore))

        number1, number2 = GeneratePredictionNumbers(todayGoldenList.goldenNumberList, lastScore, state.numbers)

        if (state.numbers == 2):

            submitRsp = client.request(

                app.op['Submit'](

                    uid=userId,

                    rid=state.roundId,

                    n1=str(number1),

                    n2=str(number2)

                ))

            if submitRsp.status == 200:

                print('You submit numbers: ' + str(number1) + ', ' + str(number2))

            else:

                print('Error: ' + submitRsp.data.message)

                time.sleep(1)



        else:

            submitRsp = client.request(

                app.op['Submit'](

                    uid=userId,

                    rid=state.roundId,

                    n1=str(number1)

                ))

            if submitRsp.status == 200:

                print('You submit number: ' + str(number1))

            else:

                print('Error: ' + submitRsp.data.message)

                time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--room', type=int, help='Room ID', required=False)

    args = parser.parse_args()

    main(args.room)