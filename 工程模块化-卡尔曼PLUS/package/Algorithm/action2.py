import os
import numpy as np
import readNum as rs
#由于调用py命令行，所以需要path，导入了os包
path = os.path.split(os.path.realpath(__file__))[0] + '\\goldenNum.txt'


#方法名和参数无所谓，随便定义
def caclute(goldenNumberList):
    #内部算法随便写，只要最后返回两个值（可以相同）即可
    # 扰动数
    number = 28
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
    with open(r'kalman.txt', 'w') as f:
        f.write(str(number1))
    print(str(number1) + ',' + str(number2))

#此处执行外部方法，不做修改为好
caclute(rs.readFile(path))
