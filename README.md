# XiuSearch

### 简介
XiuSearch是一款搜索技术博客的搜索引擎，当然，如果你将种子网址换成新闻网站，这就是一个新闻搜索引擎，它对于文章搜索来说是通用的。

[演示](http://justin3go.cc/)

> 如果网址失效，下方视频中也有演示的效果.

[视频介绍链接](https://www.bilibili.com/video/BV16m4y1X78V)

项目架构图

![image-20220122123051493](https://webplus-cn-shenzhen-s-6130b804f968dd14cecc43e2.oss-cn-shenzhen.aliyuncs.com/blogs/image-20220122123051493.png)

### 功能
+ 历史记录与搜索建议
+ 检索使用elasticsearch→快
  + 倒排索引
  + 向量空间模型与布尔模型
  + 关键词高亮
+ Swagger文档(采用前后端分离开发)
+ 适合搜索引擎的爬虫
+ 断点续爬
+ 分页显示
+ JWT登录
+ 邮箱注册(重置密码、重置邮箱)
+ pagerank
+ 正文标题提取
+ 列表页详情页区分
+ redis统计实时爬取数量(没有展示在前端)


### 主要技术栈
+ Scrapy 2.5.1
+ ElasticSearch 7.15.2
+ Django 3.1
+ DjangoRestFramework 3.12
+ Vue3

### 相关算法
+ PageRank
+ 投票机制实现内容提取
+ SVM二分类模型区分列表页与详情页

### 安装教程

```python
# 这个是直接导出的完整环境
pip install -r requirments -i https://pypi.tuna.tsinghua.edu.cn/simple  
# 这个是我印象中使用的技术栈，也可以直接安装这个
pip install -r requirments_ -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 使用说明

1. 修改根目录的config.py，其中包含elasticsearch,mysql,redis的配置(这里省略这三部分的安装，请自行百度google)。

2. 修改/Backend/Backend/settings.py

   ```python
   # 修改数据库配置
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'PASSWORD': 'xxxxxx',
           'NAME': 'xxxx',
           'USER': 'xxxx',
       }
   }
   # 修改邮箱配置
   # EMAIL CONFIG
   EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
   EMAIL_HOST = "smtp.qq.com"
   EMAIL_HOST_USER = "justin3go@qq.com"
   EMAIL_HOST_PASSWORD = "xxxxxxx"  # 这个不是qq密码，需要自己去qq邮箱申请
   EMAIL_PORT = 25
   # 如果部署，则需要如下配置，原因是阿里云不支持25端口发邮件
   EMAIL_USE_TLS = True
   EMAIL_PORT = 465 
   DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
   ```

3. 爬取数据

   ```shell
   cd ./Crawler
   scrapy crawl blog1
   ```

4. 运行django

   ```shell
   cd ./Backend
   # 迁移数据库
   python manage.py makemigrations
   python manage.py migrate
   # 运行
   python manage.py runserver
   # 打开localhost:8000/api/v1/docs/ 可以看到swagger文档
   效果应该和 http://justin3go.cc:8000/api/v1/docs/ 一样
   ```

5. 运行vue

   ```shell
   cd fontend
   npm run serve
   ```

   
