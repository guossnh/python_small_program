#-*- coding : utf-8 -*-
#新版的淘宝这边的程序计算。
#拼多多有的功能大约都要添加一下  合拍单子的情况需要根据比例计算清楚

import pandas as pd
import numpy as np
import time,os,datetime,glob,sys,csv,xlrd,re
import urllib.request