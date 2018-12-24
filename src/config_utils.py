from configobj import ConfigObj


class ConfigUtils:

    def __init__(self):
        self.config = ConfigObj('./config.ini', encoding='UTF8')
        self.url_config=self.config["wechart_url"]