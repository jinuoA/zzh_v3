#! /usr/bin/env python
# -*-coding:utf-8 -*-
import hashlib
import json
import re
import time
import traceback

import requests
from lxml import etree
from scrapy import Request

from zzh.logconf import logger
from zzh.date_format import get_publish_date
from zzh.gettitle import GetTitle
from zzh.items import ZZHSpiderItem
from zzh.scrapy_redis.spiders import RedisCrawlSpider


class BasesCrawler(RedisCrawlSpider):
    name = 'zzhbase'
    redis_key = 'basescrawler:rules'

    def __init__(self, *args, **kwargs):
        # domain = kwargs.pop('domain', '')
        # self.allowed_domains = filter(None, domain.split(','))
        # print(self.allowed_domains,'22222')
        super(BasesCrawler, self).__init__(*args, **kwargs)
        self.global_namespace = {
            "hashlib": hashlib,
            "requests": requests,
            "etree": etree,
            "GetTitle": GetTitle,
            "get_publish_date": get_publish_date,
            "traceback": traceback,
            "json": json,
            "re": re,
            "logger": logger,
            "time": time
        }

    def parse(self, response):
        try:
            item = ZZHSpiderItem()
            next_filter = response.meta.get('next_filter', '0')
            dept_id = response.meta.get('dept_id', None)
            dept_name_key = response.meta.get('dept_name_key', None)
            func = response.meta.get('func', None)
            try:
                exec(func, self.global_namespace)
                parse_spider = self.global_namespace['parse_spider']
                item_list, next_page_url = parse_spider(response, dept_id, dept_name_key)
                if item_list:
                    for it in item_list:
                        item['item_title'] = it.get('item_title', None)
                        item['item_url'] = it.get('item_url', None)
                        item['task_id'] = it.get('task_id', None)
                        item['item_pulishdate'] = it.get('item_pulishdate', None)
                        item['dept_name_key'] = it.get('dept_name_key', None)
                        item['content_xpath'] = it.get('content_xpath', None)
                        item['dept_id'] = it.get('dept_id', None)
                        yield item
                else:
                    info = f"脚本错误[未获取数据,请修改此脚本]:{response.meta['dept_name_key']}{'      '}{response.url}"
                    logger.info(info)
                    logger.info(traceback.format_exc())
                if next_page_url:
                    for next_page in next_page_url:
                        next_page = response.urljoin(next_page)
                        next_filter = bool(int(next_filter))
                        yield Request(next_page, self.parse, meta=response.meta,
                                      dont_filter=next_filter)
            except:
                info = f"脚本错误:{response.meta['dept_name_key']}{'      '}{response.url}"
                logger.info(info)
                logger.info(traceback.format_exc())
        except Exception as e:
            logger.info(e)
