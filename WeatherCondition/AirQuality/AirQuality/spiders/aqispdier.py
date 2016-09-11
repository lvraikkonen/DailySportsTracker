# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from AirQuality.items import AirqualityItem
from scrapy.selector import Selector
from datetime import datetime
import re


class AirQualitySpider(CrawlSpider):
    name = "AqiSpider"
    allowed_domains = ['aqicn.org']
    start_urls = ['http://aqicn.org/city/beijing/en/']

    def parse(self, response):
        sel = Selector(response)
        updateTime = sel.xpath(
            '//div[@style="font-size:16px;font-weight:light;;"][1]/text()').extract()
        updateTime = updateTime[0].split()[3]

        sites = sel.xpath('//div[@class="aqivalue"][1]')
        #///*[@id="cur_pm25"]
        city = sel.xpath('//title')

        url = response.url
        url = url[22:len(url) - 4]

        dt = datetime.now()

        items = []

        for site in sites:
            item = AirqualityItem()
            item['']
