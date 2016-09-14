# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import os

# mongodb driver
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class AirqualityPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]


    def process_item(self, item, spider):
        # outPath = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())),'historical_data', 'aqi')  # output path
        # file_name = 'Aqi_' + item['city'] + '_' + item['date'] + '_' + item['time'] +'.json'
        # file_path = os.path.join(outPath, file_name)

        # print os.path.join(outPath, file_name)

        # self.file = open(file_path, 'wb')

        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line)

        # save data into mongodb
        valid = True
        if not item:
            valid = False
            raise DropItem("Missing {0}".format(item))
        if valid:
            self.collection.insert(dict(item))
            log.msg("an aqi data added to MongoDB database!", level=log.DEBUG, spider=spider)
        
        return item