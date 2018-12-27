import requests
import json
import re
from .models import VisitLog


def visit_count(func):
    def wrapper(request, *args, **kwargs):
        ip = request.META['REMOTE_ADDR']
        r = requests.get('http://api.map.baidu.com/location/ip', params={'ip': ip, 'ak': 'AYoKrAimWKyh83BgdbOF8gBAOeBlmlVe'})
        content = r.content
        try:
            location = json.loads(content)['content']['address_detail']['city']
        except KeyError:
            location = '内网IP'
        page = func.__name__
        VisitLog.objects.create(pages=page, ip=ip, location=location)
        return func(request, *args, **kwargs)
    return wrapper


# 正则匹配
def re_find(re_list, content, is_list=False):
    urls_pat = re.compile(re_list, re.DOTALL)
    alist = re.findall(urls_pat, content)
    if alist:
        return alist if is_list else alist[0]
    else:
        return ""
