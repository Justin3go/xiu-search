from elasticsearch_dsl import connections, Document, Keyword, Text, Integer, Date, Completion, analyzer, Float
import sys
sys.path.append("C:\My_app\code\咻Search")
from config import ES_HOST

connections.create_connection(hosts=[ES_HOST])

my_analyzer = analyzer('ik_smart')


class BlogsIndex(Document):
    suggest = Completion(analyzer=my_analyzer)
    page_url = Keyword()
    title = Text(analyzer="ik_max_word")
    keywords = Text(analyzer="ik_max_word")
    description = Text(analyzer="ik_max_word")
    content = Text(analyzer="ik_max_word")
    PR = Float()
    publish_time = Date()

    class Index:
        name = 'blogs'


if __name__ == "__main__":
    BlogsIndex.init()
