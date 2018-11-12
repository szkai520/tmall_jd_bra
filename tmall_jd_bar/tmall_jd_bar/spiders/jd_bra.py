# -*- coding: utf-8 -*-
import json
import re

import scrapy


# https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv116&productId=25595932681&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1
from ..items import TmallJdBarItem


class JdBraSpider(scrapy.Spider):
    name = 'jd_bra'
    # allowed_domains = ['www.jd.com']
    start_urls = ['https://search.jd.com/Search?keyword=%E8%83%B8%E7%BD%A9&enc=utf-8&wq=%E8%83%B8%E7%BD%A9']

    def parse(self, response):
        braID_list = response.xpath('//div[@id="J_goodsList"]/ul/li/@data-sku').extract()
        # print(braID_list)
        for braID in braID_list:
            for i in range(21):
                url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv116&' \
                      'productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(braID, i)
                # print(url)
                yield scrapy.Request(url, callback=self.parse_jd_details)
                # break
            # break

    def parse_jd_details(self, response):
        detail_dict = response.text.replace('fetchJSON_comment98vv116(','').replace(');','')
        detail_dict = json.loads(detail_dict)
        detail_list = detail_dict['comments']
        for detail in detail_list:
            item = TmallJdBarItem()
            item['rateDate'] = detail['creationTime']
            item['rateContent'] = detail['content']
            item['color'] = detail['productColor']
            item['size'] = detail['productSize']
            item['platform'] = '京东'
            yield item
