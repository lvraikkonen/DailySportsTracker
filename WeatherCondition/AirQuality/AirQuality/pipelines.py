# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import os

class AirqualityPipeline(object):


    def process_item(self, item, spider):
        outPath = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())),'historical_data', 'aqi')  # output path
        file_name = 'Aqi_' + item['city'] + '_' + item['date'] + '_' + item['time'] +'.json'
        file_path = os.path.join(outPath, file_name)

        print os.path.join(outPath, file_name)

        self.file = open(file_path, 'wb')

        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item