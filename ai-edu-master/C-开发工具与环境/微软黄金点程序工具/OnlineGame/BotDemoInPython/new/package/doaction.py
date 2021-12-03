from package import *
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
RL = ql.QLTable(actions=list(range(7)))

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