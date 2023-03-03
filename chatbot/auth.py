import os
import sys
import base64
import random
import time
import datetime
import openai

def auth0(target):
    try:
        size = len(target)
        start = 0
        SEP = 10
        step = size//SEP
        sepStr = []
        for i in range(0,step):
            start = i*SEP
            sepStr.append(target[start:start+SEP])
        if start+SEP<size:
            sepStr.append(target[start+SEP:start+SEP+SEP])
        # print(sepStr)
        target = ''.join(sepStr[::-1])+"="*(size%4)
        # print(target)
        dec = base64.b64decode(target)
        dec = str(dec).split('\'')[1]
        tt = int(dec.split("_")[0])
        tnow = int(time.time())
        kk = "expire key"
        code = 413
        if tt<tnow:
            return kk,0,""
        expireTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tt))
        days = int((tt-tnow)/3600.0/24)
        sk = "sk-"+dec.split("_")[2].split("-")[0]
        return sk,days,expireTime
    except:
        return "not key",0,""

def auth1(api_key):
    try:
        openai.api_key = api_key
        openai.Model.list()
        return True
    except:
        return False
