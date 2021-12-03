from pyswagger import App
from pyswagger.contrib.client.requests import Client

import random
import time
import argparse
import os
import package.doaction as do
import package.QLCore as ql
import package.networkApi as gos

import numpy as np
import pandas as pd


#傻逼python 导包导我一百年，一百年！tm的 爆粗口
#有多傻逼？ 在外面的main同样的导包语句路径，本来该在外面的三个模块同样导入，居然tm跟瞎子一样，一个都不认识
#你们三个还真是几岁的儿子了？？？？！tm的，main是你们爹啊 main怎么就认得init哥导入的这些模块 你们tm一个都不认识 什么鬼逻辑
#我开始怀念java了，java导包真爽 c#更爽！


