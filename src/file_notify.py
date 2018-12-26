#
#文件系统监听工具
#     *能够对Linux系统文件系统进行监控
#     *监控信息可自动通过微信推送(需要登录)
#     *推送账号需要在程式启动时进行登录
#     *主要推送模块在
#
#
#
#
import os
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


def startFileNotify(path,wechat):
    print("选择监听目录为"+str(path)+"--即将进行监听")
    watch_manager=pyinotify.WatchManager()
    watch_manager.add_watch(path,pyinotify.ALL_EVENTS,rec=True)
    notify_event=NotifyEvent(wechat)
    notify = pyinotify.Notifier(watch_manager,notify_event)
    print("文件监听服务启动完毕....感谢使用..我是Icodeeeee...下次再见......")
    notify.loop()
class RequestUtils:
    lass_var=None
    @staticmethod
    def getDefault():
        if RequestUtils.lass_var==None:
            RequestUtils.lass_var = RequestUtils()
        return RequestUtils.lass_var
    def sendGet(self,url):
        response=requests.get(url=url,allow_redirects=False)
        response.encoding = 'utf-8'
        return response
    def sendGetForCookie(self,url,cookies):
        response=requests.get(url=url,allow_redirects=False,cookies=cookies)
        response.encoding = 'utf-8'
        return response
    #发送json请求
    def sendPost(self,url,headers,data,cookies):
        headers['content-type']='application/json; charset=UTF-8'
        r=requests.post(url=url,headers=headers,json=data,cookies=cookies)
        r.encoding = 'utf-8'
        return r
class NotifyEvent(pyinotify.ProcessEvent):
    log="---请注意:服务器文件更新---\n\n\n%s\n\n\n%s"
    def __init__(self,wechat):
        self.wechat=wechat
    def process_IN_ACCESS(self,event):
        #文件被访问==>侦听不到文件夹访问
        # self.wechat.sendTextMessage("文件被访问",'filehelper')
        print(os.path.join(event.path, event.name)+"文件被访问")
    def process_IN_CREATE(self,event):
        #创建文件夹
        print("创建文件夹")
        self.wechat.sendTextMessage(NotifyEvent.log % (os.path.join(event.path, event.name),"***[ 新增文件 ]***"), 'filehelper')
    def process_IN_MOVE(self,event):
        self.wechat.sendTextMessage(NotifyEvent.log % (os.path.join(event.path, event.name),"***[ 改动文件 ]***"), 'filehelper')
        # self.wechat.sendTextMessage("文件被移走", 'filehelper')
    def process_IN_DELETE(self, event):
        # 文件被移走
        self.wechat.sendTextMessage(NotifyEvent.log % (os.path.join(event.path, event.name),"***[ 删除文件 ]***"), 'filehelper')
        print("文件被移走")
class WechartUtils():
    # 入参url配置文件
    log="·······"
    static_obj = None
    @staticmethod
    def getDefault(config):
        if WechartUtils.static_obj==None:
            WechartUtils.static_obj = WechartUtils(config)
        return WechartUtils.static_obj
    def __init__(self, config):
        self.config = config
        pass
    def _showCommandLineQRCode(self, qr_data, enableCmdQR=2):
        try:
            b = u'\u2588'
            sys.stdout.write(b + '\r')
            sys.stdout.flush()
        except UnicodeEncodeError:
            white = 'MM'
        else:
            white = b
        black = '  '
        blockCount = int(enableCmdQR)
        if abs(blockCount) == 0:
            blockCount = 1
        white *= abs(blockCount)
        if blockCount < 0:
            white, black = black, white
        sys.stdout.write(' ' * 50 + '\r')
        sys.stdout.flush()
        qr = qr_data.replace('0', white).replace('1', black)
        sys.stdout.write(qr)
        sys.stdout.flush()
    # 入参path二维码保存地址
    def getQr(self):
        # 获取请求UUID URL地址
        get_qr_url = self.config["qr_uuid"] % time.time()
        # 获取UUID
        self.uuid = RequestUtils.getDefault().sendGet(get_qr_url).text.split("\"")[1]
        if (self.uuid == None):
            print("获取UUID失败")
            return

        try:
            # 获取二维码成功
            qrCode = QRCode('https://login.weixin.qq.com/l/' + self.uuid)
            self._showCommandLineQRCode(qrCode.text(1))
            return True
        except:
            print("写入文件失败")
    def getLoginUrl(self):
        while True:
            response=RequestUtils.getDefault().sendGet(str(self.config["get_cookie"]) % (self.uuid,time.time()))
            resp_str=response.text
            if resp_str.find("408")!=-1:
                print("二维码等待扫描中...请尽快扫描")
            elif resp_str.find("201")!=-1:
                print(self.log+"OK"+self.log+"二维码已扫描...请尽快确认")
            elif resp_str.find("200") != -1:
                print(self.log + "OK" + self.log + "恭喜你登陆成功......")
                login_url = re.search(r'(?<=").*?(?=")', resp_str).group()
                return login_url

    # 登录并获取cookie,响应为最近联系人
    def getLogingCookie(self,url):
        self.BaseRequest= dict()
        response=RequestUtils.getDefault().sendGet(url)
        print(self.log+"获取重要XML成功")
        self.login_cookie=response.cookies
        self.BaseRequest['Skey'] = re.search(r'(?<=<skey>).*?(?=</skey>)', response.text).group()
        self.BaseRequest['Sid'] = re.search(r'(?<=<wxsid>).*?(?=</wxsid>)', response.text).group()
        self.BaseRequest['Uin'] = int(re.search(r'(?<=<wxuin>).*?(?=</wxuin>)', response.text).group())
        self.pass_ticket = re.search(r'(?<=<pass\_ticket>).*?(?=</pass\_ticket>)', response.text).group()
        self.BaseRequest['DeviceID']='e' + repr(random.random())[2:17]
        #初始化请求e785569402656290
        data={}
        data["BaseRequest"]=json.dumps(self.BaseRequest)
        r= RequestUtils.getDefault().sendPost(url=self.config["init_post"]%self.pass_ticket,headers={},data=data,cookies=self.login_cookie)
        all_msg=r.text
        # 获取个人信息
        self.me_message = json.loads(all_msg)["User"]
        print(self.log+"获取个人信息成功")
        return all_msg
    def getFriendList(self):
        return RequestUtils.getDefault().sendGetForCookie(self.config["get_friend_list"] % (self.BaseRequest["Skey"]),self.login_cookie)
    def sendTextMessage(self,msg_content,toUser):
        url = self.config["send_message"] % self.pass_ticket
        clientMsgId = str(int(time.time() * 1000)) + \
                      str(random.random())[:5].replace('.', '')
        params = {
            'BaseRequest': self.BaseRequest,
            'Msg': {
                "Type": 1,
                "Content": msg_content,
                "FromUserName": self.me_message['UserName'],
                "ToUserName": toUser,
                "LocalID": clientMsgId,
                "ClientMsgId": clientMsgId
            }
        }
        headers = {'content-type': 'application/json; charset=UTF-8'}
        data = json.dumps(params, ensure_ascii=False).encode('utf8')
        r = requests.post(url, data=data, headers=headers)
        dic = r.json()
        print("推送信息:"+msg_content)
        return dic['BaseResponse']['Ret']
    def autoRun(self):
        try:
            self.getQr()
            cookie_url= self.getLoginUrl()
            self.getLogingCookie(cookie_url)
            print("开始获取好友列表-----请等待")
            self.getFriendList().text
            print("获取好友列表成功"+self.log+"将进行联系人检索并测试消息发送-发送内容为->微信通知注册成功->目标为filehelper文件传输助手")
            if self.sendTextMessage("微信通知注册成功",'filehelper')==0:
                print("测试消息发送成功====>即将启动文件监听")
                return [True,self]
            else:
                print("测试消息发送失败====>即将终止程序")
                return [False,None]
        except RuntimeError:
            print("操作异常")

class ConfigUtils:

    def __init__(self):
        self.config = ConfigObj('./config.ini', encoding='UTF8')
        self.url_config=self.config["wechart_url"]
configutils=ConfigUtils()

if __name__ == '__main__':
    # 初始化微信工具
    print("..您好..文件侦听服务准备启动")
    wechat= WechartUtils.getDefault(configutils.url_config).autoRun()
    if wechat[0]:
        # startFileNotify("/data/share",wechat[1])
        #监听目录列表  可多选
        startFileNotify(["/data/share/Share"],wechat[1])