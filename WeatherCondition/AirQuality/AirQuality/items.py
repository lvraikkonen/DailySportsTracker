# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AirqualityItem(scrapy.Item):
    date = scrapy.Field()
    time = scrapy.Field()
    area = scrapy.Field()
    aqi = scrapy.Field()
    quality = scrapy.Field()
    primary_pollutant = scrapy.Field()
    pm2_5 = scrapy.Field()
    pm10 = scrapy.Field()
    co = scrapy.Field()
    no2 = scrapy.Field()
    o3 = scrapy.Field()
    so2 = scrapy.Field()
