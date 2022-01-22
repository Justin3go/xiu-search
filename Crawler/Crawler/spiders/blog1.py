import sys
sys.path.append("C:/My_app/code/咻Search/Engine")
from Crawler.items import DetailItem, ListItem
from urllib import parse
import re
import scrapy
from url_parser import is_static_url
from gerapy_auto_extractor.extractors.title import extract_title
from gerapy_auto_extractor.extractors.datetime import extract_datetime
from gerapy_auto_extractor.classifiers.detail import is_detail
from gerapy_auto_extractor.classifiers.list import is_list
from html_extractor import MainContent

# from lxml.html.clean import Cleaner


class Blog1Spider(scrapy.Spider):
    name = 'blog1'
    # allowed_domains = ['*']
    start_urls = ['https://www.51cto.com/',
                  'https://www.iteye.com/', 'https://www.cnblogs.com/',
                  'http://www.blogjava.net/','https://blogread.cn//it/',
                  'http://blog.chinaunix.net/', 'https://www.oschina.net/',
                  'http://blog.itpub.net/', 'https://cuiqingcai.com/',
                  'http://blog.jobbole.com/', 'https://segmentfault.com/',
                  'https://www.infoq.cn/','https://www.v2ex.com/',
                  'https://www.jianshu.com/','https://blogs.360.cn/',
                  'https://tech.meituan.com/','http://www.ruanyifeng.com/blog/',
                  'http://it.deepinmind.com/','https://coolshell.cn/',
                  'https://imzl.com/','https://www.itzhai.com/',
                  'http://macshuo.com/','http://ifeve.com/',
                  'http://blog.zhaojie.me/','https://juejin.cn/',
                  'https://www.runoob.com/']

    # 规则
    rule_encode = "//meta/@charset"
    rule_keywords = "//meta[@name='keywords']/@content"
    rule_description = "//meta[@name='description']/@content"
    rule_lang = "//@lang"
    rule_url = "//@href"  # 简答地提取url的规则
    # 保留标签的 src 属性
    # safe_attrs = frozenset(['src'])
    # 删除 a 标签
    # remove_tags = frozenset(['script','style','link'])
    # 实例化
    # cleaner = Cleaner(
    #     style=True,
    #     scripts=True,
    #     javascript=True,
    #     meta=False,
    #     # safe_attrs=safe_attrs,
    #     # remove_tags=remove_tags,
    # )

    def parse(self, response):
        page_url = response.request.url
        print("-"*100)
        print("开始爬取%s......" % page_url)
        if response.status == 200:
            # cleaned_html = self.cleaner.clean_html(response.body.decode('utf-8'))
            # with open("./test.html", 'w', encoding="utf-8") as f:
            #     f.write(str(cleaned_html))
            # sys.exit()
            # 获取内容
            encode = response.xpath(self.rule_encode).extract()
            keywords = response.xpath(self.rule_keywords).extract()
            description = response.xpath(self.rule_description).extract()
            lang = response.xpath(self.rule_lang).extract()
            # 这里代码检测有问题，实际没问题，只能说VS有点垃圾，继承关系都搞不懂
            publish_time = extract_datetime(response.body.decode('utf-8'))

            urls = response.xpath(self.rule_url).extract()
            urls_cleaned = []
            for url in urls:
                if is_static_url(url) or "javascript:" in url.lower():
                    continue
                # 绝对链接不变，相对链接转换为绝对链接
                full_url = parse.urljoin(page_url, url)
                urls_cleaned.append(full_url)

            # 如果符合详情页规则，就下载该网页,提取其正文
            if is_detail(response.body, 0.3):
                print("该网页符合详情页规则.....")
                print("提取[ %s ]携带的正文标题中......" % page_url)

                extractor = MainContent()
                title, content = extractor.extract(page_url, response.body)

                # 保存...
                detail_item = DetailItem()
                detail_item['page_url'] = page_url
                detail_item['encode'] = encode
                detail_item['keywords'] = keywords
                detail_item['description'] = description
                detail_item['lang'] = lang
                detail_item['title'] = title
                detail_item['content'] = content
                detail_item['urls'] = urls_cleaned
                detail_item['publish_time'] = publish_time

                yield detail_item

            # 如果不符合详情页规则，就下载该网页,不提取其正文
            elif is_list(response.body, 0.9):
                print("该网页符合列表页规则.....")
                # 保存...
                list_item = ListItem()
                list_item['page_url'] = page_url
                list_item['encode'] = encode
                list_item['keywords'] = keywords
                list_item['description'] = description
                list_item['lang'] = lang
                list_item['urls'] = urls_cleaned
                list_item['publish_time'] = publish_time

                yield list_item
            else:
                print("跳过爬取!!!!!!")

            for url in urls_cleaned:
                yield scrapy.Request(url=url, callback=self.parse)

        else:
            print("[ %s ]未爬取成功......" % page_url)
            return
