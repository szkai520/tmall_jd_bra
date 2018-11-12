# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TmallJdBarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rateDate = scrapy.Field()
    rateContent = scrapy.Field()
    color = scrapy.Field()
    size = scrapy.Field()
    platform = scrapy.Field()
