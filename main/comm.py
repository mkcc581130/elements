import requests
import json
import re
from datetime import datetime
from .models import VisitLog, IPList


def visit_count(func):
    def wrapper(request, *args, **kwargs):
        ip = request.META['REMOTE_ADDR']
        try:
            ip_info = IPList.objects.get(ip=ip)
            location = ip_info.location
            ip_info.last_login = datetime.now()
            ip_info.save()
        except IPList.DoesNotExist:
            r = requests.get(url='http://ipquery.market.alicloudapi.com/query', params={'ip': ip},
                             headers={'Authorization': 'APPCODE 2635ec67fea14b06b064a5b08b9b49f7'})
            content = r.content
            try:
                location = json.loads(content)['data']['city']
            except KeyError:
                location = '内网IP'
            IPList.objects.create(ip=ip, location=location)
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
