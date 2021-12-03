import os
import numpy as np
import random
import readNum as rs
#由于调用py命令行，所以需要path，导入了os包
path = os.path.split(os.path.realpath(__file__))[0] + '\\goldenNum.txt'


#方法名和参数无所谓，随便定义
def caclute(gArray):
    #内部算法随便写，只要最后返回两个值（可以相同）即可
    if len(gArray) == 0:
        number1 = 28
        number2 = 28
    if len(gArray) != 0:
        number1 = 50*0.618 + random.uniform(1,30 * 0.618)
        number2 = 50/30*0.618 + np.average(gArray[-5:])
    print(str(number1) + ',' + str(number2))

#此处执行外部方法，不做修改为好
caclute(rs.readFile(path))
