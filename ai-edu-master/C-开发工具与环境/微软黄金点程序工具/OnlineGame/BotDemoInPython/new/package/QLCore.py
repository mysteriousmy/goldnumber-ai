from new.package import *

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