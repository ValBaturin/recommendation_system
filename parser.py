#!/usr/bin/python3
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
from urllib.request import quote, urlopen
import io

class LinkParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._in_nobullet = False
        self._store = []

    def handle_starttag(self, tag, attrs):
        if tag == 'ul':
            attrs = dict(attrs)
            if attrs.get('class') == 'nobullet':
                self._in_nobullet = True
        if self._in_nobullet and tag == 'a':
            self._store.append('https://www.entrepreneur.com' + attrs[0][1])

    def handle_endtag(self, tag):
        if self._in_nobullet and tag == 'ul':
            self._in_nobullet = False

    def parse(self, page):
        self.feed(page)
        return self._store

class ArticleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        #article args
        self._text = io.StringIO()
        self._in_div_tag = False
        self._in_text_tag = False
        self._misleading_div = 0
        self._is_important = False
        #title args
        self._in_head_tag = False
        self._in_h1_tag = False

    def handle_starttag(self, tag, attrs):
        #article
        if tag == 'div':
            attrs = dict(attrs)
            if attrs.get('class') == 'bodycopy':
                self._in_div_tag = True
            elif self._in_div_tag:
                self._misleading_div += 1
        if self._in_div_tag:
            if tag == 'p':
                self._in_text_tag = True
            if tag == 'h2':
                self._in_text_tag = True
                self._is_important = True
        if self._in_div_tag and tag == 'strong':
            self._in_strong = True
        #title
        if tag == 'article':
            attrs = dict(attrs)
            if attrs.get('class') == 'main':
                self._in_head_tag = True
        if self._in_head_tag and tag == 'h1':
            self._in_h1_tag = True

    def handle_endtag(self, tag):
        #article
        if self._in_div_tag and tag == 'div' and self._misleading_div == 0:
            self._in_div_tag = False
        if self._misleading_div and tag == 'div':
            self._misleading_div -= 1
        if self._in_text_tag and (tag == 'p' or tag == 'h2'):
            self._in_text_tag = False
            self._is_important = False
        #title
        if self._in_head_tag and tag == 'article':
            self._in_head_tag = False
        if self._in_h1_tag and tag == 'h1':
            self._in_h1_tag = False

    def handle_data(self, data):
        #article
        if self._is_important:
            self._text.write('\n')
        if self._in_text_tag:
            self._text.write(str(data).strip())
        #title
        if self._in_h1_tag:
            self._text.write(data)

    def parse(self, page):
        self.feed(page)
        return self._text.getvalue()

def get_article(page):
    return ArticleParser().parse(page)

def get_links(html):
    return LinkParser().parse(html)
