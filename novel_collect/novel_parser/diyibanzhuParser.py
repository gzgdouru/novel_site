import requests
import os, re
from urllib import parse
from lxml import etree

from dataStructures import EXCEPTION_PREFIX, NovelInfo, ChapterInfo

BASE_URL = "http://www.diyibanzhu.one/"


def get_html_text(url, encoding, timeout):
    response = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0'
    }, timeout=timeout)
    response.encoding = encoding

    if not response.text:
        raise RuntimeError("{0}获取[{1}]内容失败!".format(EXCEPTION_PREFIX, url))

    return response.text


def parse_info(url, encoding="gbk", timeout=30):
    '''提取小说信息(网站名称, 作者, 简介, 详细介绍)(供采集调用)'''
    try:
        htmltree = etree.HTML(get_html_text(url, encoding, timeout))

        site = htmltree.xpath("//div[@class='left_con']/ul/li[1]/a/text()")[0]
        # novel = htmltree.xpath("//div[@class='j_box']/div[@class='title']/h2/text()")[0]
        author = htmltree.xpath("//div[@class='j_box']/div[@class='info']/ul/li[1]/a/text()")[0]
        intro = htmltree.xpath("//div[@class='j_box']/div[@class='words']/p/text()")[1]
        detail = intro
        intro = (intro[:252] + "...") if len(intro) > 255 else intro
    except Exception as e:
        raise RuntimeError("{0}diyibanzhuParser::parse_info({1})失败, 原因:{2}".format(EXCEPTION_PREFIX, url, e))

    if not author:
        raise RuntimeError("{0}diyibanzhuParser::parse_info({1})失败, 原因:小说作者为None!".format(EXCEPTION_PREFIX, url))

    return NovelInfo(site=site, author=author, intro=intro, detail=detail)


def parse_chapter(url, encoding="gbk", timeout=30):
    '''解析小说章节(供采集调用)'''
    try:
        htmltree = etree.HTML(get_html_text(url, encoding, timeout))
        chapters = htmltree.xpath("//div[@class='list_box']/ul/li/a")
        for chapter in chapters:
            chapterUrl = parse.urljoin(url, chapter.get("href"))
            charpterName = chapter.text
            yield ChapterInfo(url=chapterUrl, name=charpterName)
    except Exception as e:
        raise RuntimeError("{0}diyibanzhuParser::paser_chapter({1})失败, 原因:{2}".format(EXCEPTION_PREFIX, url, e))


def parse_test(url, encoding="gbk", timeout=30):
    '''解析测试(供采集调用)'''
    try:
        chapters = parse_chapter(url, encoding=encoding, timeout=timeout)
        for chapter in chapters:
            return True
    except Exception as e:
        raise RuntimeError("{0}diyibanzhuParser:parse_test({1})失败, 原因: {2}".format(EXCEPTION_PREFIX, url, e))
    raise RuntimeError("{0}diyibanzhuParser:parse_test({1})失败, 原因: 提取章节信息失败!".format(EXCEPTION_PREFIX, url))


def parse_sub_content(url, encoding="gbk", timeout=30):
    '''解析章节的小节内容'''
    try:
        htmltree = etree.HTML(get_html_text(url, encoding, timeout))
        content = htmltree.xpath("//div[@class='box_box']/text()")
    except Exception as e:
        raise RuntimeError("{0}diyibanzhuParser:parse_sub_content({1})失败, 原因: {2}".format(EXCEPTION_PREFIX, url, e))
    return content


def parse_content(url, encoding="gbk", timeout=30):
    '''解析小说内容(供采集调用)'''
    try:
        htmltree = etree.HTML(get_html_text(url, encoding, timeout))
        subChapters = htmltree.xpath("//div[@class='chapterPages']/a")
        contentList = []
        for chapter in subChapters:
            url = parse.urljoin(url, chapter.get("href"))
            contentList.extend(parse_sub_content(url, encoding, timeout))
    except Exception as e:
        raise RuntimeError("{0}diyibanzhuParser:parse_content({1})失败, 原因: {2}".format(EXCEPTION_PREFIX, url, e))
    return "<br>\n".join(contentList)


if __name__ == "__main__":
    url = r'http://www.diyibanzhu.one/0/11209/'
    if parse_test(url):
        print(True)
    else:
        print(False)
