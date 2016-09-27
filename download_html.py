#!/usr/bin/python3
# -*- coding: utf-8 -*-


import argparse
import log
from urllib.request import urlopen
from urllib.error import URLError
from os.path import isfile
import concurrent
from concurrent.futures import ThreadPoolExecutor
import sys

from config import HTML_PATH
import parser


class Date():
    def __init__(self, month, year):
        self.month = month
        self.year = year

    def __le__(self, other):
        return  self.year < other.year or (self.year == other.year and self.month <= other.month)

    def next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1

    def dates_until(self, other):
        while self <= other:
            yield self
            self.next()

    def to_link(self):
        monthes = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        return 'https://www.entrepreneur.com/sitemaps/' + str(self.year) + '/' + monthes.get(self.month) + '/us'



def load(url):
    try:
        response = urlopen(url)
    except URLError as e:
        log.error('Can\'t load %s, %s', url, e.reason)
    else:
        if response.code == 200:
            html = str(response.read(), encoding='utf-8')
            log.debug('Load %s: %s', url, response.code)
            return html
        else:
            log.error('Load %s: %s', url, response.code)

class UrlGenerator():
    def __init__(self, start, finish = None):
        if not finish:
            finish = start
        self.start = Date(*map(int, start.split('.')))
        self.finish = Date(*map(int, finish.split('.')))

    def date_html_gen(self):
        for date in self.start.dates_until(self.finish):
            link = date.to_link()
            yield load(link)

    def get_article_links(self):
    	article_links = []
    	for date_html in self.date_html_gen():
    		article_links += parser.get_links(date_html)
    	return article_links


def load_url(url):
    html = load(url)
    if not html:
        return
    file_path = HTML_PATH + url.lstrip('https://www.entrepreneur.com/article/')
    if isfile(file_path):
        log.debug('File \"%s\"" exists already', file_path)
        return
    with open(file_path, 'w') as out:
        print(html, file=out)
        log.debug("Create \"%s\" file", file_path)

def parse_argument(argv):
    parser = argparse.ArgumentParser(
        description = 'Download articles from entrepreneur website.'
    )
    parser.add_argument(
        help = 'input mm.yyyy as a date which will be crawled',
        dest = 'start'
        )
    parser.add_argument(
        '--untill',
        default = None,
        help = 'to download bunch of articles from date to date do not forget to input mm.yyyy as the date that will be the last included',
        dest = 'finish'
        )
    parser.add_argument(
        '--thread',
        type = int,
        default = 20,
        help = 'number of threads',
        dest = 'thread_number'
    )
    parser.add_argument(
        '--log',
        default = 'debug',
        help = 'log level',
        choices = ['critical', 'error',  'debug'],
        dest = 'log_level'
    )

    return parser.parse_args()


def main():
    args = parse_argument(sys.argv)
    log.config(log.level(args.log_level))
    url_list = (UrlGenerator(args.start, args.finish).get_article_links())
    log.debug('STARTING...')
    with ThreadPoolExecutor(max_workers=args.thread_number) as executor:
        result = executor.map(load_url, url_list)
    log.debug('...FINISHED')

if __name__ == '__main__':
    main()
