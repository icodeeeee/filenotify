#
#     *文件系统监听工具
#     *能够对Linux系统文件系统进行监控
#     *监控信息可自动通过微信推送(需要登录)
#     *推送账号需要在程式启动时进行登录
#     *主要推送模块在WechartUtils中
#
############################################

启动方式 python3 file_notify.py
如果监听隐私文件请root方式运行
依赖模块

import pyinotify
import os
import re
import random
import sys

import requests
import time
import json
from configobj import ConfigObj
from pyqrcode import QRCode


############################################

		需要改进的地方	

############################################


触发通知的情况









