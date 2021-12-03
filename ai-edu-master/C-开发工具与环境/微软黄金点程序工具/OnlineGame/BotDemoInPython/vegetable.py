from pyswagger import App
from pyswagger.contrib.client.requests import Client

import random
import time
import argparse
#初始化swagger客户端
host = 'https://goldennumber.aiedu.msra.cn'
jsonpath = '/swagger/v1/swagger.json'
app = App._create_(host + jsonpath)
clinet = Client()

def GeneratePredictionNumbers(goldenNumberList, numberCount):
    
    number1 = 0.0 # 提交数
    number2 = 0.0 # 提交数2
    print(goldenNumberList) # 十组数据
    if len(goldenNumberList) == 0: # 如果数据长度为0
        number1 = 18.0  # 初始数据为18.0
        if numberCount == 2:
            number2 = 18.0 # 初始数据为18.0
    else:
        #  取前十组数据平均值
        number1 = sum(goldenNumberList[-10:]) / float(len(goldenNumberList[-10:]))
        if numberCount == 2:
            # 取前一轮黄金点做值
            number2 = goldenNumberList[-1]

    return number1, number2

def main(roomId):
    # roomId
    if roomId is None:
        roomId = input('Input room id:')
        try:
            roomId = int(roomId)
        except:
            roomId = 0
            print('Parse room id failed, default join in to room 0')
    userInfoFile = 'userinfo.txt'
    userId = None
    nickName = None
    try:
        with open(userInfoFile) as f:
            userId, nickName = f.read().split(',')[:2]
        print('Use an exist player:' + nickName + ' Id:' + userId)
    except:
        userResp = clinet.request(
            app.op['NewUser'](
                nickName = 'AI player ' + str(random.randint(0, 9999))
            )
        )
        assert userResp.status == 200
        user = userResp.data
        userId = user.userId
        nickName = user.nickName
        print('Create a new player: ' + nickName + ' Id:' + userId)
    
        with open(userInfoFile, 'w') as f:
            f.write("%s,%s" % (userId, nickName))
    print('Room id: ' + str(roomId))
    
    while True:
        stateResp = clinet.request(
            app.op['State'](
                uid = userId,
                roomid = roomId
            )
        )
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
                time.sleep(1)
            continue
        print('\r\n This is round ' + str(state.finishedRoundCount + 1))
    
        todayGoldenListResp = clinet.request(
            app.op['TodayGoldenList'](
                roomid = roomId
            )
        )
        if todayGoldenListResp.status != 200:
            print('Network issue, query again after 1 second')
            time.sleep(1)
            continue
        todayGoldenList = todayGoldenListResp.data
        if len(todayGoldenList.goldenNumberList) != 0:
            print('Last golden number is :' + str(todayGoldenList.goldenNumberList[-1]))
        number1, number2 = GeneratePredictionNumbers(todayGoldenList.goldenNumberList, state.numbers)
        print(number1)
        if(state.numbers == 2):
            submitRsp = clinet.request(
                app.op['Submit'](
                    uid = userId,
                    rid = state.roundId,
                    n1 = str(number1),
                    n2 = str(number2)
                )
            )
            if submitRsp.status == 200:
                print('You submit numbers: ' + str(number1) + ', ' + str(number2))
            else:
                print('Error: ' + submitRsp.data.message)
                time.sleep(1)
        else:
            submitRsp = clinet.request(
                app.op['Submit'](
                    uid = userId,
                    rid = state.roundId,
                    n1 = str(number1)
                )
            )
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