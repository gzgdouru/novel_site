import os, sys, re
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import threading, time
from concurrent import futures

from parseConfig import ParseConfig
from novelLog import logger
from utils.mysqlV1 import MysqlManager
from utils.myEmail import MyEmail
from utils.sms import send_sms
from dataStructures import EXCEPTION_PREFIX


class Collect:
    def __init__(self, configFile="config.json"):
        self.load_config(configFile)
        self.init_database()
        self.init_email()
        self.init_novel()

    def load_config(self, configFile):
        logger.info("load_config() start...")
        try:
            self.config = ParseConfig(configFile)
            logger.info("load_config() complete.")
        except Exception as e:
            logger.error("load_config() failed, error:{0}".format(e))
            sys.exit(-1)

    def init_database(self):
        logger.info("init_database() start...")
        try:
            self.mydb = MysqlManager(**self.config.database)
            logger.info("init_database() complete.")
        except Exception as e:
            logger.error("init_database() failed, error:{0}".format(e))
            sys.exit(-1)

    def init_email(self):
        logger.info("init_email() start...")
        try:
            smtpServer = self.config.email.get("smtp_server")
            sender = self.config.email.get("sender")
            password = self.config.email.get("sender_passwd")
            charset = self.config.email.get("charset")
            self.myemail = MyEmail(smtpServer=smtpServer, sender=sender, senderPasswd=password, charset=charset)
            logger.info("init_email() complete.")
        except Exception as e:
            logger.error("init_email() failed, error:{0}".format(e))
            sys.exit(-1)

    def init_novel(self):
        logger.info("init_novel() start...")
        try:
            self.check_main_table()
            self.check_chapter_table()

            with futures.ThreadPoolExecutor(max_workers=10) as executor:
                for novel in self.config.novels[:]:
                    executor.submit(self.save_novel, novel)
            logger.info("init_novel() complete.")
        except Exception as e:
            logger.error("init_novel() failed, error:{0}".format(e))
            sys.exit(-1)

    def save_novel(self, novel):
        try:
            url = novel.get("url")
            novelName = novel.get("name")
            status = novel.get("status")
            charset = novel.get("charset", "gbk")
            parserName = self.config.get_parser_name(novel.get("parser"))

            # 跳过不需要解析的小说
            if not status:
                self.config.novels.remove(novel)
                return

            # 解析测试
            try:
                self.config.parsers[parserName].parse_test(url, encoding=charset)
            except Exception as e:
                logger.error("小说[{0}]解析测试失败, 原因: {1}".format(novelName, e))
                self.config.novels.remove(novel)
            else:
                logger.info("小说[{0}]解析测试成功.".format(novelName))

                # 保存小说信息到数据库
                if not self.save_novel_info(novel):
                    # 移除保存失败的小说
                    self.config.novels.remove(novel)
        except Exception as e:
            logger.error("save_novel({0})失败, 原因: {1}".format(novelName, e))

    def save_novel_info(self, novel):
        url = novel.get("url")
        novelName = novel.get("name")
        parserName = self.config.get_parser_name(novel.get("parser"))
        parser = self.config.parsers.get(parserName)
        charset = novel.get("charset", "gbk")

        try:
            novelInfo = parser.parse_info(url, encoding=charset, timeout=30)

            if not novelName or not novelInfo.author:
                logger.error("小说名称或作者名称为None!")
                return False

            # 已保存的小说直接返回
            if self.mydb.exist("tb_novel", conditions="novel_name = '{0}'".format(novelName)):
                return True

            # 获取作者ID
            conditions = "name = '{0}'".format(novelInfo.author)
            if not self.mydb.exist("tb_novel_author", conditions=conditions):
                # 注:异步运行时有可能造成冲突
                self.mydb.insert("tb_novel_author", name=novelInfo.author, intro=novelInfo.author,
                                 detail=novelInfo.author, add_time=datetime.now())
            author = next(self.mydb.select("tb_novel_author", conditions=conditions))

            # 获取'其他'分类ID
            conditions = "name = '其他'"
            if not self.mydb.exist("tb_novel_category", conditions=conditions):
                #注:异步运行时有可能造成冲突
                self.mydb.insert("tb_novel_category", name='其他', add_time=datetime.now())
            category = next(self.mydb.select("tb_novel_category", conditions=conditions))

            # 插入小说信息
            self.mydb.insert("tb_novel", novel_name=novelName, site_name=novelInfo.site, url=url, intro=novelInfo.intro,
                             add_time=datetime.now(), author_id=author.id, parser=parserName, detail=novelInfo.detail,
                             category_id=category.id)
            logger.info("保存小说({0}, url:{1}))信息成功.".format(novelName, url))
            return True
        except Exception as e:
            logger.error("保存小说({0}, url:{1}))信息失败, 原因:{2}".format(novelName, url, e))
        return False

    def check_main_table(self):
        # 检查 tb_novel_category 表是否存在
        if not self.mydb.exist("information_schema.TABLES",
                               conditions="TABLE_SCHEMA = 'novel_site' and TABLE_NAME ='tb_novel_category'"):
            raise RuntimeError("{0}数据表[tb_novel_category]不存在".format(EXCEPTION_PREFIX))

        # 检查 tb_novel 表是否存在
        if not self.mydb.exist("information_schema.TABLES",
                               conditions="TABLE_SCHEMA = 'novel_site' and TABLE_NAME ='tb_novel'"):
            raise RuntimeError("{0}数据表[tb_novel]不存在".format(EXCEPTION_PREFIX))

    def check_chapter_table(self):
        for i in range(10):
            table = "tb_chapter_{0}".format(i)
            conditions = "TABLE_SCHEMA = 'novel_site' and TABLE_NAME ='{table}'".format(table=table)
            if not self.mydb.exist("information_schema.TABLES", conditions=conditions):
                raise RuntimeError("{0}数据表[{1}]不存在!".format(EXCEPTION_PREFIX, table))
        return True

    def show_config(self):
        logger.info(self.config.show_config())

    def reset_config(self, confPath="config.json"):
        logger.info("reload config....")
        self.load_config(confPath)
        self.init_database()
        self.init_email()
        self.init_novel()
        self.parse_novel()

    def parse_novel(self):
        with futures.ThreadPoolExecutor(max_workers=self.config.base.get("novels", 1)) as executor:
            for novel in self.config.novels:
                executor.submit(self.parse_novel_thread, novel)

    def parse_novel_thread(self, novel):
        novelName = novel.get("name")

        novel_obj = next(self.mydb.select("tb_novel", conditions="novel_name = '{0}'".format(novelName)))
        if novel_obj.is_end:
            #已完结的小说不再爬取
            logger.info("小说[{0}]已完结.".format(novelName))
            return None

        logger.info("爬取小说[{0}]开始.".format(novelName))
        time_start = time.time()

        try:
            self.save_chapter(novel, novel_obj)
        except Exception as e:
            logger.error("parse_novel_thread({0})失败, 原因: {1}".format(novelName, e))
        finally:
            time_end = time.time()
            logger.info("爬取小说[{0}]结束. 耗时:{1}".format(novelName, time_end - time_start))

    def get_chapter_table_by_name(self, novelName):
        '''根据小说名称获取章节表'''
        novel = next(self.mydb.select("tb_novel", conditions="novel_name = '{0}'".format(novelName)))
        return "tb_chapter_{0}".format(novel.id % 10)

    def get_chapter_table_by_id(self, novelId):
        '''根据小说id获取章节表'''
        return "tb_chapter_{0}".format(int(novelId) % 10)

    def update_notice(self, novelId, novelName):
        '''更新通知'''
        try:
            for fav in self.mydb.select("tb_user_fav", conditions="novel_id = {0} and notice_enable = 1".format(novelId)):
                user = next(self.mydb.select("tb_user_profile", conditions="id = {0}".format(fav.user_id)))
                content = "[天天悦读]你收藏的小说({0}), 已经更新了.".format(novelName)
                if user.email:
                    self.myemail.set_receiver([user.email])
                    subject = "小说更新通知"
                    stderr = self.myemail.send_email(subject, content)
                    if stderr:
                        logger.error("send email to [{0}] failed:{1}".format(user.username, stderr))
                    else:
                        logger.info("send email to [{0}] success.".format(user.username))
                elif user.mobile:
                    send_sms(user.mobile, novelName)
                    logger.info("semd sms to [{0}] success.".format(user.username))
                else:
                    self.mydb.insert("tb_user_message", message=content, user_id=user.id, is_read=0,
                                     add_time=datetime.now())
                    logger.info("write message to [{0}] success.".format(user.username))

        except Exception as e:
            logger.error("update_notice({0}) error:{1}".format(novelName, str(e)))

    def save_chapter(self, novel, novel_obj):
        '''保存章节信息'''
        charset = novel.get("charset")
        parserName = self.config.get_parser_name(novel.get("parser"))

        try:
            table = self.get_chapter_table_by_id(novel_obj.id)
            urls = list(self.get_all_chapter_url(table, novel_obj.id))

            #创建小说目录
            path = os.path.join(self.config.base.get("file_root"), str(novel_obj.id))
            if not os.path.exists(path):
                os.makedirs(path)

            has_update = False
            parser = self.config.parsers.get(parserName)

            with futures.ThreadPoolExecutor(max_workers=self.config.base.get("chapters", 1)) as executor:
                for chapter in parser.parse_chapter(novel_obj.url, encoding=charset):
                    if chapter.url in urls:
                        #跳过已经保存的章节
                        continue
                    has_update = True
                    executor.submit(self.save_chapter_thread, parser, chapter, novel_obj)

            if has_update:
                # 发送更新通知
                self.update_notice(novel_obj.id, novel_obj.novel_name)
        except Exception as e:
            raise RuntimeError("{0}保存小说({1})章节失败, 原因: {2}".format(EXCEPTION_PREFIX, novel_obj.novel_name, e))

    def save_chapter_thread(self, parser, chapter, novel_obj):
        try:
            # 生成文件
            path = os.path.join(self.config.base.get("file_root"), str(novel_obj.id))
            content = parser.parse_content(chapter.url)
            self.write_content(path, chapter.url, content=content)

            table = self.get_chapter_table_by_id(novel_obj.id)

            # 保存到数据库
            self.mydb.insert(table, novel_id=novel_obj.id, chapter_url=chapter.url,
                             chapter_index=self.get_chapter_index(chapter.url),
                             chapter_name=chapter.name, add_time=datetime.now())
            logger.info("save [{0}({1})] to [{2}] success.".format(novel_obj.novel_name, chapter.name, table))
        except Exception as e:
            raise RuntimeError("{0}save_chapter_thread({1})失败, 原因: {2}".format(EXCEPTION_PREFIX, chapter.url, e))

    def get_all_chapter_url(self, table, novelId):
        result = self.mydb.select(table, conditions="novel_id = {0}".format(novelId))
        for r in result:
            yield r.chapter_url

    def get_chapter_index(self, chapterUrl):
        pos = chapterUrl.rfind("/")
        chapterIndex = re.match(r"\d+", chapterUrl[pos + 1:]).group()
        return int(chapterIndex)

    def write_content(self, path, chapterUrl, content):
        try:
            name = "{0}.txt".format(self.get_chapter_index(chapterUrl))
            fullPath = os.path.join(path, name)
            with open(fullPath, "w", encoding="utf-8") as fileObj:
                fileObj.write(content)
        except Exception as e:
            raise RuntimeError("{0}write_content({1}) error:{2}".format(EXCEPTION_PREFIX, fullPath, e))

    def run(self):
        while True:
            self.parse_novel()
            time.sleep(1 * 60)


if __name__ == "__main__":
    collect = Collect()
    collect.run()
