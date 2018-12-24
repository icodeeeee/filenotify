import re
import requests
import time

from src.network.network_utils import RequestUtils


class WechartUtils():
    # 入参url配置文件
    log="·······"
    def __init__(self, config):
        self.config = config
        return

    # 入参path二维码保存地址
    def getQr(self, path):
        # 获取请求UUID URL地址
        get_qr_url = self.config["qr_uuid"] % time.time()
        # 获取UUID
        self.uuid = RequestUtils.getDrfault().sendGet(get_qr_url).text.split("\"")[1]
        if (self.uuid == None):
            print("获取UUID失败")
            return
        # 获取二维码成功
        qr_file = RequestUtils.getDrfault().sendGet(self.config["qr_url"] + self.uuid).content
        try:
            f = open(path, 'wb+')
            f.write(qr_file)
            f.close()
            print("获取文件成功"+self.log+"已写入" + path+"\n请打开文件准备扫码")
            return True
        except:
            print("写入文件失败")
    def getLoginUrl(self):
        while True:
            response=RequestUtils.getDrfault().sendGet(str(self.config["get_cookie"]) % (self.uuid,time.time()))
            resp_str=response.text
            if resp_str.find("408")!=-1:
                print("二维码等待扫描中...请尽快扫描")
            elif resp_str.find("201")!=-1:
                print(self.log+"OK"+self.log+"二维码已扫描...请尽快确认")
            elif resp_str.find("200") != -1:
                print(self.log + "OK" + self.log + "恭喜你登陆成功......")
                print(resp_str)
                login_url = re.search(r'(?<=").*?(?=")', resp_str).group()
                return login_url

    def autoRun(self):
        self.getQr("./qr.png")
        print(self.getLoginUrl())