from fake_useragent import UserAgent
import time
import sys
sys.path.append("C:/My_app/code/咻Search")


BOT_NAME = 'Crawler'
SPIDER_MODULES = ['Crawler.spiders']
NEWSPIDER_MODULE = 'Crawler.spiders'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = UserAgent().random
# Obey robots.txt rules
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 0.5
COOKIES_ENABLED = False
ITEM_PIPELINES = {
    'Crawler.pipelines.MysqlTwistedPipeline': 200,
    'Crawler.pipelines.ElasticSearchPipeline': 300,
}
# Broad Crawls --广泛的爬取官网推荐的设置
# 应用推荐的优先级队列
SCHEDULER_PRIORITY_QUEUE = 'scrapy.pqueues.DownloaderAwarePriorityQueue'
# 增加并发--Scrapy 下载器将执行的最大并发（即同时）请求数。
CONCURRENT_REQUESTS = 100
# 增加 Twisted IO 线程池最大大小
REACTOR_THREADPOOL_MAXSIZE = 20
# 降低日志级别
LOG_LEVEL = 'INFO'
# 禁用 cookie
COOKIES_ENABLED = False
# 禁用重试
RETRY_ENABLED = False
# 减少下载超时
DOWNLOAD_TIMEOUT = 15
# 禁用重定向
REDIRECT_ENABLED = False
# 启用“Ajax 可抓取页面”的抓取
AJAXCRAWL_ENABLED = True

# My Settings
# 爬行深度
DEPTH_LIMIT = 10
# log
LOG_FILE = "all.log"
now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
JOBDIR="breakpoints/" + str(now_time)


