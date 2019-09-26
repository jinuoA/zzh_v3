# -*- coding:utf -*-
import random

import requests
from lxml import etree
from zzh.conf.user_agents import agents


class GetTitle(object):

    def __init__(self):
        self.user_agent = agents

    def getTit(self, url, title_xpath):
        page = requests.get(url, headers={'User-Agent': random.choice(self.user_agent)})
        page.encoding = 'utf-8'
        page = page.text
        page = etree.HTML(page)
        try:
            title = page.xpath(title_xpath)
            title = title[0]
            return title
        except:
            title = ''
            return title



