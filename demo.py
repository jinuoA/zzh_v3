#! /usr/bin/env python
# -*-coding:utf-8 -*-
from zzh.conf.db_helper import DBHelper
from zzh.conf.db_settings import scriptDb
import os

db = DBHelper(scriptDb)
# sql = "select * from zzh_projectruler where dept_name_key like '51%'"
# sql = "select * from zzh_projectruler"
sql = "select dept_id,dept_name_key,func,url,project_desc from zzh_projectruler"
sql_p = "select province_name,area_code from zzh_province"
sql_c = "select city_name,area_code from zzh_city"
sql_d = "select district_name,area_code from zzh_district"


def demo():
    result = db.select(sql)
    for i in result:
        print(i)
        fc = i[8].replace("print p", "#print p").replace("print t", "#print t").replace("print next_page_url",
                                                                                        "print (next_page_url)").replace(
            "print s", "#print s").replace("'", "\\'").replace("update(task_id)",
                                                               'update(task_id.encode("utf-8"))').replace('%', '%%')
        # fc = i[8].replace("print p","#print p").replace("'","\\'")
        spider_id = i[0]
        # print(spider_id)
        # print(fc)
        sql_a = "update zzh_projectruler set func='%s' where id=%s" % (fc, spider_id)
        db.update(sql_a)


def deletePrint():
    result = db.select(sql)
    for i in result:
        spider_script = i[8]
        spider_list = spider_script.split('\r\n')
        spider_new_script = ""
        for spider in spider_list:
            if "print" in spider:
                spider = ""
            elif "except:" in spider:
                sp = spider.split("except")[0] + "    "
                # info = '''info = "脚本错误:" + "    " + response.url + "    " + response.meta['dept_name_key']'''
                # spider = (spider + "\r\n" + sp +info + "\r\n" + sp + "logger.info(info)")
                spider = (spider + "\r\n" + sp + "pass")
            spider_new_script += (spider + "\r\n")
        spider_new_script = spider_new_script.replace("'", "\\'").replace("dept_id.encode('utf-8')", "dept_id").replace(
            "title.encode('utf-8')", "title").replace("update(task_id)", 'update(task_id.encode("utf-8"))').replace('%',
                                                                                                                    '%%')
        print(spider_new_script)
        spider_id = i[0]
        sql_a = "update zzh_projectruler set func='%s' where id=%s" % (spider_new_script, spider_id)
        db.update(sql_a)


def exportScript():
    for r in db.select(sql):
        dept_id = r[0]
        dept_name_key = r[1]
        func = r[2].strip()
        url = r[3]
        project_desc = r[4]
        scriptStr = f"""
#! /usr/bin/env python
#-*-coding:utf-8 -*-

import redis
import json

strl = '''

{func}

'''
        
data_list = [
    {{
        "spider": "zzhbase",
        "project": "zzh",
        "dept_id": "{dept_id}",
        "dept_name_key": "{dept_name_key}",
        "url": "{url}",
        "func": strl,
        "next_filter": '0'
    }}

]
        
for data in data_list:
    reminder_str = json.dumps(data)
    r = redis.StrictRedis(host='192.168.5.127', port=6381, db=0)
    print(r.lpush('basescrawler:rules', reminder_str))
        """
        province = dept_name_key[:4]
        city = dept_name_key[:6]
        district = dept_name_key[:6]
        for p in db.select(sql_p):
            if str(p[1])[:4] == province:
                path = os.path.join("F:\spider_demo\zzh_v3\spiderScriptPyThree", p[0], p[0])
                isExists = os.path.exists(path)
                if not isExists:
                    os.makedirs(path)
                with open(f'{path}/{project_desc}.py','w',encoding='utf-8') as f:
                    f.write(scriptStr)
            if str(p[1])[:2] == province[:2]:
                for c in db.select(sql_c):
                    if str(str(c[1])[:6]) == city:
                        path = os.path.join("F:\spider_demo\zzh_v3\spiderScriptPyThree", p[0], c[0],c[0])
                        print(path)
                        isExists = os.path.exists(path)
                        if not isExists:
                            os.makedirs(path)
                        with open(f'{path}/{project_desc}.py', 'w', encoding='utf-8') as f:
                            f.write(scriptStr)
                    if str(c[1])[:4] == city[:4]:
                        for d in db.select(sql_d):
                            if str(str(d[1])[:6]) == district:
                                path = os.path.join("F:\spider_demo\zzh_v3\spiderScriptPyThree", p[0], c[0],d[0])
                                print(path)
                                isExists = os.path.exists(path)
                                if not isExists:
                                    os.makedirs(path)
                                with open(f'{path}/{project_desc}.py', 'w', encoding='utf-8') as f:
                                    f.write(scriptStr)








# deletePrint()


def makeDir():
    for r in db.select(sql):
        dept_name_key = r[1]
        province = dept_name_key[:2] + "00"
        city = dept_name_key[:4]
        for p in db.select(sql_p):
            if str(p[1])[:4] == province:
                for c in db.select(sql_c):
                    if str(str(c[1])[:4]) == city:
                        path = os.path.join("F:\spider_demo\zzh_v3\spiderScriptPyThree", p[0], c[0])
                        isExists = os.path.exists(path)
                        if not isExists:
                            os.makedirs(path)
                    # elif str(p[1])[:4] == province:
                    #     path = os.path.join("F:\spider_demo\zzh_v3\spiderScriptPyThree", p[0], p[0])
                    #     print(path)
                    #     isExists = os.path.exists(path)
                    #     if not isExists:
                    #         os.makedirs(path)

"""

province = dept_name_key[:4]
        city = dept_name_key[:4]
        for p in db.select(sql_p):
            if str(p[1])[:4] == province:
                path = os.path.join("F:\spider_demo\zzh_v3\spiderScriptPyThree", p[0], p[0])
                isExists = os.path.exists(path)
                if not isExists:
                    os.makedirs(path)
                with open(f'{path}/{project_desc}.py','w',encoding='utf-8') as f:
                    f.write(scriptStr)
            if str(p[1])[:2] == province[:2]:
                for c in db.select(sql_c):
                    if str(str(c[1])[:4]) == city:
                        path = os.path.join("F:\spider_demo\zzh_v3\spiderScriptPyThree", p[0], c[0])
                        print(path)
                        isExists = os.path.exists(path)
                        if not isExists:
                            os.makedirs(path)
                        with open(f'{path}/{project_desc}.py', 'w', encoding='utf-8') as f:
                            f.write(scriptStr)

"""


# makeDir()
exportScript()
