#! /usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
from scrapy.utils.project import get_project_settings  # 导入seetings配置
import sys


class DBHelper():
    '''这个类也是读取settings中的配置，自行修改代码进行操作'''

    def __init__(self,db):

        self.host = db.get("MYSQL_HOST")
        self.port = db.get("MYSQL_PORT")
        self.user = db.get("MYSQL_USER")
        self.passwd = db.get("MYSQL_PASSWD")
        self.db = db.get("MYSQL_DBNAME")



    # 连接到mysql，不是连接到具体的数据库
    def connectMysql(self):
        conn = pymysql.connect( host = self.host,
                                port = self.port,
                                user = self.user,
                                passwd = self.passwd,
                                # db=self.db,不指定数据库名
                                charset = 'utf8' )  # 要指定编码，否则中文可能乱码
        return conn

    # 连接到具体的数据库（settings中设置的MYSQL_DBNAME）
    def connectDatabase(self):
        conn = pymysql.connect( host = self.host,
                                port = self.port,
                                user = self.user,
                                passwd = self.passwd,
                                db = self.db,
                                charset = 'utf8' )  # 要指定编码，否则中文可能乱码
        return conn

    # 创建数据库
    def createDatabase(self):
        '''因为创建数据库直接修改settings中的配置MYSQL_DBNAME即可，所以就不要传sql语句了'''
        conn = self.connectMysql()  # 连接数据库

        sql = "create database if not exists " + self.db
        cur = conn.cursor()
        cur.execute( sql )  # 执行sql语句
        cur.close()
        conn.close()

    # 创建表
    def createTable(self, sql):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute( sql )
        cur.close()
        conn.close()

    # 查询数据
    def select(self, sql):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute( sql )
        # 获取所有记录
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    # 插入数据
    def insert(self, sql, *params):  # 注意这里params要加*,因为传递过来的是元组，*表示参数个数不定
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute( sql, params )
        conn.commit()  # 注意要commit
        cur.close()
        conn.close()

    # 更新数据
    def update(self, sql, *params):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute( sql, params )
        conn.commit()  # 注意要commit
        cur.close()
        conn.close()

    # 删除数据
    def delete(self, sql, *params):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute( sql, params )
        conn.commit()
        cur.close()
        conn.close()
