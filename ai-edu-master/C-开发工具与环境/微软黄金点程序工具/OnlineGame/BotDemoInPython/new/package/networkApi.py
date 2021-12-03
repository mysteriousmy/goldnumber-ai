import new.package

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
            print('上一轮的分数是：{}'.format(lastScore))

            number1, number2 = do.GeneratePredictionNumbers(todayGoldenList.goldenNumberList, lastScore, state.numbers)
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
                        do.RL.cleanAll()
                        continue
                    time.sleep(1)