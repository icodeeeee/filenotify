#程序启动器
from src.config_utils import ConfigUtils
from src.wechart.wechart_login import WechartUtils

configutils=ConfigUtils()
if __name__=='__main__':
    #初始化微信工具
    print("工具初始化")
    wechar_utils=WechartUtils(configutils.url_config)
    wechar_utils.autoRun()
