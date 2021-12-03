'''
该文件仅作算法书写规范示例
'''
import os
import numpy as np
import math

#方法名和参数无所谓，随便定义
def kalman(data = [1,2,3,4,5,6,7,8,9,10,11,12,13], predictnumber = 8):

    """
    卡尔曼滤波算法
    :param data:
    :return:
    """

    #  print(len(data))
    lastValue = data[-5:]+[predictnumber]
    # 上五次的最优估计值
    # last_H = math.sqrt(MAX_Error**2+MIN_Error**2)
    # 最后一次的噪声，暂时不用好了
    n_ = lastValue[1] - lastValue[0]

    #  初始误差
    """
    初始随机估计值
    """
    estimatedValue = lastValue[0] * 0.618
    #  初始估计值
    optimalValue = estimatedValue
    #  print(optimalValue)
    #  初始下轮最优估算值
    for i in range(len(lastValue) - 1):
        last_H = (lastValue[i + 1] - lastValue[i]) * 0.618*0.5
        #  print(last_H)
        #  获得本次观察偏差
        rightValue = lastValue[i + 1]
        #  观察值
        H = math.sqrt(last_H ** 2 + n_ ** 2)
        #  偏差
        HPlus = math.sqrt(H ** 2 / (H ** 2 + last_H ** 2))
        #  协方差
        optimalValue = optimalValue + HPlus * (rightValue - optimalValue)
        print(optimalValue)
        #  print(optimalValue)
        #  更新最优估计值
        # print((1 - H) * (H ** 2))
        n_ = math.sqrt((abs(1 - H)) * (H ** 2))
        #  更新初始偏差，作为下一轮的初始偏差
        pass

    #  predictNumber = optimalValue + HPlus * (data[-1] - optimalValue)
    #  由于无法得到最后一次，即提交时的观测值，只能用粗略估计值代替
    #  print(optimalValue)
    return optimalValue

    pass

