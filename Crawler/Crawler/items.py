import scrapy
from Crawler.models.es_blogs import BlogsIndex
from Crawler.utils.common import real_time_count

# 统计索引的数据
COUNT_INIT = 0


class DetailItem(scrapy.Item):
    page_url  = scrapy.Field()  # 当前网页的url
    
    encode = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    lang = scrapy.Field()
    
    title = scrapy.Field()
    content = scrapy.Field()
    publish_time = scrapy.Field() 
    
    urls = scrapy.Field()  # 包含的url
    
    def save_to_mysql(self):
        # 插入的sql语句
        insert_sql = """
                   insert into search_blogs(page_url, urls)
                   VALUES (%s, %s)
               """     
        
        sql_params = (
            str(self['page_url']) or 'NAN', str(self['urls']) or 'NAN'
        )
        return insert_sql, sql_params
    
    def save_to_es(self):
        blogs = BlogsIndex()
        blogs.suggest = self['title']   # 为title建立建议字段
        blogs.page_url = self['page_url']
        blogs.title = self['title']
        blogs.keywords = self['keywords']
        blogs.description = self['description']
        blogs.content = self['content']
        blogs.publish_time = self['publish_time']

        real_time_count('view_count', COUNT_INIT)
        blogs.save()
        print("已建立索引到elasticsearch中......")

    def help_fields(self):
        for field in self.fields:
            print(field, "= scrapy.Field()")


class ListItem(scrapy.Item):
    # 列表页不需要存内容以及标题，并且暂时不用建立索引，保存到数据库中就可以了
    page_url  = scrapy.Field()  # 当前网页的url
    
    encode = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    lang = scrapy.Field()
    
    publish_time = scrapy.Field() 
    
    urls = scrapy.Field()  # 包含的url
    
    def save_to_mysql(self):
        # 插入的sql语句
        insert_sql = """
                   insert into search_list(page_url, urls)
                   VALUES (%s, %s)
               """
        sql_params = (
            str(self['page_url']) or 'NAN', str(self['urls']) or 'NAN'
        )

        return insert_sql, sql_params
    

    def help_fields(self):
        for field in self.fields:
            print(field, "= scrapy.Field()")