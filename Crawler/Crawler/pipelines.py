# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from Crawler.items import DetailItem, ListItem
import codecs,os,json
import copy
import pymysql
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from config import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD


class ElasticSearchPipeline(object):
    """通用的ElasticSearch存储方法"""

    def process_item(self, item, spider):
        # 只有详情页才加索引
        if isinstance(item, DetailItem):
            item.save_to_es()
        return item
    
class MysqlTwistedPipeline(object):
    
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, crawler):
        # 读取settings中的配置
        params = dict(
            host=MYSQL_HOST,
            db=MYSQL_DBNAME,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False
        )
        # 创建连接池，pymysql为使用的连接模块
        dbpool = adbapi.ConnectionPool('pymysql', **params)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        print("已存入mysql中......")
        return item
        
    # 执行数据库操作的回调函数
    def do_insert(self, cursor, item):
        sql, params = item.save_to_mysql()
        cursor.execute(sql, params)

    # 当数据库操作失败的回调函数
    def handle_error(self, failue, item, spider):
        print(failue)

# 使用json存到本地文件的代码
# class CrawlerPipeline:
#     def __init__(self):
#         # 必须使用 w+ 模式打开文件，以便后续进行 读写操作（w+模式，意味既可读，亦可写）
#         # 注意：此处打开文件使用的不是 python 的 open 方法，而是 codecs 中的 open 方法
#         self.json_file = codecs.open('data.json', 'w+', encoding='UTF-8')

#     def open_spider(self, spider):
#         # 在爬虫开始时，首先写入一个 '[' 符号，构造一个 json 数组
#         # 为使得 Json 文件具有更高的易读性，我们辅助输出了 '\n'（换行符）
#         self.json_file.write('[\n')
        
        
#     def process_item(self, item, spider):
#         item_json = json.dumps(dict(item), ensure_ascii=False)
#         self.json_file.write('\t' + item_json + ',\n')
#         return item

#         if isinstance(item, DetailItem):
#             page_url = item['page_url']
#             encode = item['encode']
#             keywords = item['keywords']
#             description = item['description']
#             lang = item['lang']
#             title = item['title']
#             content = item['content']
#             urls_cleaned = item['urls']
#             publish_time = item['publish_time']
#             f = open("./data.json", 'w+', encoding="utf-8")
            

#         if isinstance(item, ListItem):
#             page_url = item['page_url']
#             encode = item['encode']
#             keywords = item['keywords']
#             description = item['description']
#             lang = item['lang']
#             urls_cleaned = item['urls']
#             publish_time = item['publish_time']
            
#     # 爬虫结束时执行的方法
#     def close_spider(self, spider):
#         # 在结束后，需要对 process_item 最后一次执行输出的 “逗号” 去除
#         # 当前文件指针处于文件尾，我们需要首先使用 SEEK 方法，定位到文件尾前的两个字符（一个','(逗号), 一个'\n'(换行符)）的位置
#         self.json_file.seek(-2, os.SEEK_END)
#         # 使用 truncate() 方法，将后面的数据清空
#         self.json_file.truncate()
#         # 重新输出'\n'，并输出']'，与 open_spider(self, spider) 时输出的 '[' 相对应，构成一个完整的数组格式
#         self.json_file.write('\n]')
#         # 关闭文件
#         self.json_file.close()

