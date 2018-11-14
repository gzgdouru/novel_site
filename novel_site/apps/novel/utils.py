from bs4 import BeautifulSoup
import requests
from django.http import Http404
import os

from novel import models
from novel_site.settings import logger
from novel_site.settings import CUSTOM_NOVEL_FILE_PATH

relation = {
    "tb_chapter_0": models.Chapter0,
    "tb_chapter_1": models.Chapter1,
    "tb_chapter_2": models.Chapter2,
    "tb_chapter_3": models.Chapter3,
    "tb_chapter_4": models.Chapter4,
    "tb_chapter_5": models.Chapter5,
    "tb_chapter_6": models.Chapter6,
    "tb_chapter_7": models.Chapter7,
    "tb_chapter_8": models.Chapter8,
    "tb_chapter_9": models.Chapter9,
}


def get_chapter_table(novelId):
    tableName = "tb_chapter_{}".format(int(novelId) % 10)
    return relation.get(tableName)


def get_content(novelId, novelIndex):
    content = None
    try:
        dirPath = os.path.join(CUSTOM_NOVEL_FILE_PATH, str(novelId))
        fullPath = os.path.join(dirPath, "{0}.txt".format(novelIndex))
        with open(fullPath, "r", encoding="utf-8") as fileObj:
            content = '''
            <div id="novel_content" style="font-size: 16px;">
            {0}
            </div>
            '''.format(fileObj.read())
    except Exception as e:
        logger.error("get_content({0}:{1}) error:{2}".format(novelId, novelIndex, e))
        raise RuntimeError("内容页面解析出错!")
    return content