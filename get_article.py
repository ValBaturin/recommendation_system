#!/usr/bin/python3
# -*- coding: utf-8 -*-

from config import ROOT_PATH, HTML_PATH, ARTICLE_PATH
from parser import get_article
from os import listdir
from os.path import isfile
import log

if __name__ == "__main__":
    for html in listdir(HTML_PATH):
        if not isfile(ARTICLE_PATH + str(html)):
            with open(ARTICLE_PATH + str(html), 'w') as out, open(HTML_PATH + str(html), 'r+') as html_text:
                html_text = html_text.read()
                print(get_article(html_text), file=out)
                log.debug("Extract article from %s and save", html)
