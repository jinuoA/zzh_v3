# -*- coding: utf-8 -*-

import datetime
import socket

from zzh.logconf import logger
from kafka.client import SimpleClient
from kafka.producer import SimpleProducer
from scrapy.utils.serialize import ScrapyJSONEncoder


class KafkaPipeline(object):
    """
    Publishes a serialized item into a Kafka topic
    :param producer: The Kafka producer
    :type producer: kafka.producer.Producer
    :param topic: The Kafka topic being used
    :type topic: str or unicode
    """

    def __init__(self, producer, topic):
        """
        :type producer: kafka.producer.Producer
        :type topic: str or unicode
        """
        self.producer = producer
        self.topic = topic
        self.encoder = ScrapyJSONEncoder()
        self.tmp_list = []
        self.time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.agent_ip_port = self.getHostIp()

    def process_item(self, item, spider):
        """
        Overriden method to process the item
        :param item: Item being passed
        :type item: scrapy.item.Item
        :param spider: The current spider being used
        :type spider: scrapy.spider.Spider
        """
        item = dict(item)
        item['time_str'] = self.time_str
        item['agent_ip_port'] = self.getHostIp()
        item_title = item['item_title']
        # logger.info(item_title)
        if item_title:
            print(item_title)
            msg = self.encoder.encode(item)
            # msg = msg.encode('utf-8')
            # self.producer.send_messages(self.topic, msg)

    @classmethod
    def from_settings(cls, settings):
        """
        :param settings: the current Scrapy settings
        :type settings: scrapy.settings.Settings
        :rtype: A :class:`~KafkaPipeline` instance
        """
        k_hosts = settings.get('SCRAPY_KAFKA_HOSTS', '127.0.0.1:9092')
        topic = settings.get('SCRAPY_KAFKA_ITEM_PIPELINE_TOPIC', 'data-topic')
        client = SimpleClient(k_hosts)
        producer = SimpleProducer(client)
        return cls(producer, topic)

    def getHostIp(self):
        try:
            hostName = socket.getfqdn(socket.gethostname())
            hostAddr = socket.gethostbyname(hostName)
        finally:
            pass
        return hostAddr
