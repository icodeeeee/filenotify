import requests


class RequestUtils:
    lass_var=None
    @staticmethod
    def getDrfault():
        if RequestUtils.lass_var==None:
            RequestUtils.lass_var = RequestUtils()
            return RequestUtils.lass_var
        else:return RequestUtils.lass_var
    def sendGet(self,url):
        response=requests.get(url=url)
        return response
