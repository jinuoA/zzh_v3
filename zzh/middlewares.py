# encoding=utf-8
import datetime
import random
import time

from zzh.logconf import logger
from zzh.conf.db_helper import DBHelper
from zzh.conf.db_settings import infoDb, proxyDb


class ProxyMiddleWare(object):
    """docstring for ProxyMiddleWare"""

    def __init__(self):
        self.pdb = DBHelper(proxyDb)

    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        proxy = self.get_random_proxy()
        request.headers['Proxy-Authorization'] = proxy

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            proxy = self.get_random_proxy()
            request.meta['proxy'] = proxy
            return request
        return response

    def get_random_proxy(self):
        '''随机从文件中读取proxy'''
        proxySQl = "select ip,ip_port from proxy_url limit 30"
        result = self.pdb.select(proxySQl)
        proxies = []
        for proxy in result:
            proxyIp = f"http://{proxy[0]}:{proxy[1]}"
            proxies.append(proxyIp)
        proxy = random.choice(proxies).strip()
        return proxy


class RotateUserAgentMiddleware(object):
    """url_agent"""

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get("CUSTOM_USER_AGENT")
        )

    def process_request(self, request, spider):
        url_agent = random.choice(self.user_agent)
        if url_agent:
            request.headers.setdefault('User-Agent', url_agent)


class GetFailedUrl(object):
    def __init__(self):
        self.db = DBHelper(infoDb)

    def process_response(self, response, request, spider):
        if response.status != 200:
            queue_url = request.meta['url']
            spider_url = response.url
            status_code = response.status
            save_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dept_id = request.meta['dept_id']
            dept_name_key = request.meta['dept_name_key']
            argsList = (queue_url, spider_url, status_code, save_time, int(dept_id), dept_name_key)
            sql = """insert into spider_fail_url (queue_url,spider_url,status_code, save_time,dept_id, dept_name_key) \
                                  values('%s','%s','%s','%s',%s,'%s');""" % argsList
            self.db.insert(sql)
        else:
            return response
        return response


class RandomDelayMiddleware(object):
    def __init__(self, delay):
        self.delay = delay

    @classmethod
    def from_crawler(cls, crawler):
        delay = crawler.spider.settings.get("RANDOM_DELAY", 10)
        if not isinstance(delay, int):
            raise ValueError("RANDOM_DELAY need a int")
        return cls(delay)

    def process_request(self, request, spider):
        delay = round(random.random(), 2) + 0.20
        logger.info("### random delay: %s s ###" % delay)
        time.sleep(delay)
