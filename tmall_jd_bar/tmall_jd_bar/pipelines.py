# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as pymysql


class TmallJdBarPipeline(object):
    def open_spider(self,spider):
        self.con = pymysql.connect(host='127.0.0.1', port=3306, user='root',
                                    db='tmall_jd_bra', password='123456', charset='utf8')
        self.cur = self.con.cursor()


    def process_item(self, item, spider):
        try:
            self.cur.execute(
                'insert into bra_info (rateDate,rateContent,color,size,platform) values(%s,%s,%s,%s,%s)', (
                    item['rateDate'], item['rateContent'], item['color'], item['size'], item['platform']))
            self.con.commit()
        except Exception as e:
            print("数据存入失败")


        return item


    def close_spider(self,spider):
        self.con.close()

