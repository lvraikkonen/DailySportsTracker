# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider
from AirQuality.items import AirqualityItem
from scrapy.selector import Selector
import datetime
import time
from dateutil import parser
import re


ISOTIMEFORMAT='%Y-%m-%d %X'


class AirQualitySpider(CrawlSpider):
    name = "AqiSpider"
    download_delay = 2
    allowed_domains = ['aqicn.org']
    start_urls = ['http://aqicn.org/city/beijing/en/']

    def parse(self, response):
        # filename = response.url.split("/")[-2] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

        sel = Selector(response)

        cur_time = time.time()
        cur_time = time.strftime(ISOTIMEFORMAT, time.localtime(cur_time))

        secondsDiff = long(float(sel.xpath('//*[@id="aqiwgtutime"]/@val').extract()[0])) + 60*60  # upt + 60 minutes
        updatetime = time.strftime(ISOTIMEFORMAT, time.localtime(secondsDiff))
        # parse str into datetime
        updatetime = parser.parse(updatetime)
        city = sel.xpath('//*[@id="city0"]/span[1]/text()').extract()[0]
        aqivalue = int(sel.xpath('//*[@id="aqiwgtvalue"]/text()').extract()[0])
        aqilevel = sel.xpath('//*[@id="aqiwgtinfo"]/text()').extract()[0]

        pm25 = int(sel.xpath('//*[@id="cur_pm25"]/text()').extract()[0])
        pm10 = int(sel.xpath('//*[@id="cur_pm10"]/text()').extract()[0])
        o3 = int(sel.xpath('//*[@id="cur_o3"]/text()').extract()[0])
        no2 = int(sel.xpath('//*[@id="cur_no2"]/text()').extract()[0])
        so2 = int(sel.xpath('//*[@id="cur_so2"]/text()').extract()[0])
        co = int(sel.xpath('//*[@id="cur_co"]/text()').extract()[0])

        temp = int(sel.xpath('//*[@id="cur_t"]/span/text()').extract()[0])
        dew = int(sel.xpath('//*[@id="cur_d"]/span/text()').extract()[0])
        pressure = int(sel.xpath('//*[@id="cur_p"]/text()').extract()[0])
        humidity = int(sel.xpath('//*[@id="cur_h"]/text()').extract()[0])
        wind = int(sel.xpath('//*[@id="cur_w"]/text()').extract()[0])

        item = AirqualityItem()
        item['date'] = updatetime.strftime("%Y%m%d")
        item['hour'] = updatetime.hour # strftime("%H%M%S")
        item['city'] = city
        item['aqivalue'] = aqivalue
        item['aqilevel'] = aqilevel
        item['pm2_5'] = pm25
        item['pm10'] = pm10
        item['co'] = co
        item['no2'] = no2
        item['o3'] = o3
        item['so2'] = so2
        item['temp'] = temp
        item['dew'] = dew
        item['pressure'] = pressure
        item['humidity'] = humidity
        item['wind'] = wind
        item['crawl_time'] = cur_time

        return item
