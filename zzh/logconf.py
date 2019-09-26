#! /usr/bin/env python
# -*-coding:utf-8 -*-
import logging.config
from os import path

# log_file_path = path.join(path.dirname(path.abspath(__file__)), 'log.conf')
# print(log_file_path)
# logging.config.fileConfig(log_file_path)
# logger = logging.getLogger()

logging.config.fileConfig("zzh/log.conf")
logger = logging.getLogger("cse")
