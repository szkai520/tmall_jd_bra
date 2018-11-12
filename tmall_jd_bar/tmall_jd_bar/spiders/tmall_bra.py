# -*- coding: utf-8 -*-
import json
import re

import scrapy

from ..items import TmallJdBarItem


class TmallBraSpider(scrapy.Spider):
    name = 'tmall_bra'
    # allowed_domains = ['www.tmall.com']
    start_urls = ['https://list.tmall.com/search_product.htm?q=%D0%D8%D5%D6']

    def parse(self, response):
        """
        解析出首页每个内衣的每页评论的请求地址
        """
        braID_list = response.xpath('//div[@id="J_ItemList"]/div[@class="product  "]/@data-id').extract()
        for braID in braID_list:
            for i in range(1, 11):
                url = 'https://rate.tmall.com/list_detail_rate.htm?itemId={}&' \
                      'sellerId=1813097055&order=3&currentPage={}&append=0&content=1&' \
                      'tagId=&posi=&picture=&groupId=&callback=jsonp3452'.format(braID, i)
                # print(url)
                yield scrapy.Request(url, callback=self.parse_details)
                # break
            # break

    def parse_details(self, response):
        """
        解析每条数据的属性
        rateDate:评论时间
        rateContent:评论内容
        color:内衣颜色
        size:内衣大小
        platform:购买平台
        """
        detail_dict = response.text.replace('jsonp3452(', '').replace(')', '')
        detail_dict = json.loads(detail_dict)
        detail_list = detail_dict['rateDetail']['rateList']
        for detail in detail_list:
            item = TmallJdBarItem()
            item['rateDate'] = detail['rateDate']
            item['rateContent'] = detail['rateContent']
            color_size = re.split('[:;]', detail['auctionSku'])
            item['color'] = color_size[1]
            item['size'] = color_size[3]
            item['platform'] = detail['cmsSource']
            yield item

