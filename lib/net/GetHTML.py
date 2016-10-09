#! python3
import re
import requests

a_link = re.compile(
    r'<(a|link) (([^\'"]+?=[^\'"]+?|[^\'"]+?=\'[^\'"]+?\'|[^\'"]+?="[^\'"]+?") *)*'
    r'href=([-_.~!*\'();:@&=+$,/?#%\[\]A-Za-z0-9]+?|'
    r'\'[-_.~!*\'();:@&=+$,/?#%\[\]A-Za-z0-9]+?\'|'
    r'"[-_.~!*\'();:@&=+$,/?#%\[\]A-Za-z0-9]+?") *'
    r'(([^\'"]+?=[^\'"]+?|[^\'"]+?=\'[^\'"]+?\'|[^\'"]+?="[^\'"]+?") *)*/?>'
)
img_link = re.compile(
    r'<img (([^\'"]+?=[^\'"]+?|[^\'"]+?=\'[^\'"]+?\'|[^\'"]+?="[^\'"]+?") *)*'
    r'src=([-_.~!*\'();:@&=+$,/?#%\[\]A-Za-z0-9]+?|'
    r'\'[-_.~!*\'();:@&=+$,/?#%\[\]A-Za-z0-9]+?\'|'
    r'"[-_.~!*\'();:@&=+$,/?#%\[\]A-Za-z0-9]+?") *'
    r'(([^\'"]+?=[^\'"]+?|[^\'"]+?=\'[^\'"]+?\'|[^\'"]+?="[^\'"]+?") *)*/?>'
)
css_link = re.compile(
    r'url\(([-_.~!*\'();:@&=+$,/?#%\[\]A-Za-z0-9]+?|'
    r'\'[-_.~!*\'();:@&=+$,/?#%\[\]A-Za-z0-9]+?\'|'
    r'"[-_.~!*\'();:@&=+$,/?#%\[\]A-Za-z0-9]+?")\)'
)


class GetHTML:
    header = {}
    cookie = {}
    __req = requests.session()

    @staticmethod
    def get(url, header=None, cookie=None, timeout=10, session=True, reset_session=False):
        header = header if header is not None else {}
        cookie = cookie if cookie is not None else {}
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

    @staticmethod
    def get_links(html):
        return {
            'link': [
                link[3][1:-1] if link[3][0] == '\'' or link[3][0] == '"' else link[3]
                for link in a_link.findall(html)
            ],
            'image': [
                link[2][1:-1] if link[2][0] == '\'' or link[2][0] == '"' else link[2]
                for link in img_link.findall(html)
            ],
            'css_image': [
                link[1:-1] if link[0] == '\'' or link[0] == '"' else link
                for link in css_link.findall(html)
            ]
        }
