# -*- coding: utf-8 -*-
import scrapy
import argparse
import re
from scrapy import signals
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess


class CrewlSpider(CrawlSpider):
    name = 'crewl'
    allwords = []
    rules = (Rule(LinkExtractor(), follow=True, callback='parse_item'),)

    # Use this to override the behaviour when the crawler finishes.
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(CrewlSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def __init__(self, url, file, *args, **kwargs):
        super(CrewlSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.allowed_domains = [self.get_allowed(url)]
        self.file = file

    def get_allowed(self, url):
        return re.findall('^(?:https?:\/\/)?(?:[^@\/\n]+@)?([^:\/\n]+)', url)[0]

    def spider_closed(self, spider):
        # for item in self.allwords:
        #     print(item)
        #     self.file.write(item)
        # self.file.close()
        print(self.allwords)
        for item in self.allwords:
            self.file.write(item)
            self.file.write(b'\n')
        self.file.close()

    def __update_allwords(self, words):
        self.allwords += words
        self.allwords = sorted(set(self.allwords))

    def __getwords(self, response):
        words = []
        alltxt = ''
        for item in response.xpath('//text()'):
            txt = item.get()
            alltxt += txt
            # Filter characters
            txt = re.sub('[\(\),./"\'?!“”‘’]', ' ', txt)
            # Replace all spacers with one space
            txt = re.sub('\s+', ' ', txt)
            # Transform to lowercase
            txt = txt.lower()
            # Convert to bytes
            txt = txt.encode()
            # Split the words
            words += txt.split(b' ')

        # Unique
        words = sorted(set(words))
        # Remove empty string and if the string is not longer than 1 char.
        words = [i for i in words if ((i != '') and (len(i) > 1))]
        self.__update_allwords(words)
        return words

    def parse_item(self, response):
        #Only process 'text'
        #Convert to lowercase for easy matching
        h = {k.lower():v for k,v in response.headers.items()}
        if (b'content-type' in h.keys()) and (b'text/html' in h[b'content-type'][0]):
            try:
                # Return the result
                yield {'url': response.url,
                       'title': response.css('title::text').get(),
                       'words:': self.__getwords(response),
                       }
            except Exception as e:
                yield {'url': response.url,
                       'title': '',
                       'error': str(e),
                       }
        else:
            print(h[b'content-type'])
            return

def main():
    parser = argparse.ArgumentParser(
        description='Crawl a website and grab some words.')
    parser.add_argument('url', help='The url to be crawled')
    parser.add_argument('file', help='The file to write the output to', type=argparse.FileType(mode='wb'))
    args = parser.parse_args()
    print(args.file)

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        # 'LOG_ENABLED': False
        # 'LOG_LEVEL' : 'CRITICAL'
    })

    process.crawl(CrewlSpider, url=args.url, file=args.file)
    process.start()


if __name__ == '__main__':
    main()
