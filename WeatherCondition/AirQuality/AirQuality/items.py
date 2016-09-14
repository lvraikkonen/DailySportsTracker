# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AirqualityItem(scrapy.Item):
    date = scrapy.Field()
    hour = scrapy.Field()
    city = scrapy.Field()
    # area = scrapy.Field()
    aqivalue = scrapy.Field()
    aqilevel = scrapy.Field()
    pm2_5 = scrapy.Field()
    pm10 = scrapy.Field()
    co = scrapy.Field()
    no2 = scrapy.Field()
    o3 = scrapy.Field()
    so2 = scrapy.Field()
    temp = scrapy.Field()
    dew = scrapy.Field()
    pressure = scrapy.Field()
    humidity = scrapy.Field()
    wind = scrapy.Field()

    # add field to log spider crawl time
    crawl_time = scrapy.Field()
