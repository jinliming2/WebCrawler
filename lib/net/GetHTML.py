#! python3
import requests


class GetHTML:
    header = {}
    cookie = {}
    __req = requests.session()

    @staticmethod
    def get(url, header=None, cookie=None, timeout=10, session=True, reset_session=False):
        if reset_session:
            GetHTML.reset_session()
        req = GetHTML.__req if session else requests
        try:
            r = req.get(url, headers=header, cookies=cookie, timeout=timeout)
        except requests.Timeout as e:
            print(e)
            raise
        return r.text

    @staticmethod
    def reset_session():
        GetHTML.__req.close()
        GetHTML.__req = requests.session()
        GetHTML.__req.headers.update(GetHTML.header)
        GetHTML.__req.cookies.update(GetHTML.cookie)
