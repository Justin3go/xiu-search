from config import ES_HOST
from datetime import datetime

from elasticsearch import Elasticsearch

from django.utils.datastructures import OrderedSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from search_blogs.models import BlogsIndex
import sys
sys.path.append("C:/My_app/code/咻Search")
# Create your views here.
# class IndexView(View):
#     pass

client = Elasticsearch(hosts=[ES_HOST])


class SearchView(APIView):
    '''
    返回搜索结果的接口
    '''
    permission_classes = [AllowAny]

    q = openapi.Parameter('q',
                          openapi.IN_QUERY,
                          description="查询语句",
                          type=openapi.TYPE_STRING)
    p = openapi.Parameter('p',
                          openapi.IN_QUERY,
                          description="页码",
                          type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[q, p], responses={200: {}})
    def get(self, request):
        # 获取参数
        key_words = request.query_params.get("q", "")
        page = request.query_params.get("p", "1")
        # key_words = q
        # s_type = ["title", "keywords", "description", "content"]
        # page = p

        try:
            page = int(page)
        except:
            page = 1
        try:
            start_time = datetime.now()  # 计时
            response = client.search(index="blogs",
                                     body={
                                         "query": {
                                             "multi_match": {
                                                 "query": key_words,
                                                 "fields":
                                                 ["title", "content"]
                                             }
                                         },
                                         "from": (page - 1) * 10,
                                         "size": 10,
                                         "highlight": {
                                             "pre_tags":
                                             ["<span class='highlight'>"],
                                             "post_tags": ["</span>"],
                                             "fields": {
                                                 "title": {},
                                                 "content": {},
                                             },
                                             "fragment_size":
                                             40
                                         }
                                     })
            end_time = datetime.now()
            search_cost_time = (end_time - start_time).total_seconds()

            total_nums = response["hits"]["total"]["value"]

            if (total_nums % 10) > 0:
                page_nums = int(total_nums / 10) + 1
            else:
                page_nums = int(total_nums / 10)

            hit_list = []
            # 这里封装的时候也可以重新排序-->不过elastic里面应该有，后面可以看看
            for hit in response["hits"]["hits"]:
                hit_dict = {}
                # title
                if "title" in hit["highlight"]:
                    hit_dict["title"] = "".join(hit["highlight"].get(
                        "title", ""))
                else:
                    hit_dict["title"] = hit["_source"].get("title", "")

                # content
                if "content" in hit["highlight"]:
                    hit_dict["content"] = "".join(hit["highlight"].get(
                        "content", ""))  # 取前五百个词
                else:
                    hit_dict["content"] = hit["_source"].get("content", "")

                hit_dict["page_url"] = hit["_source"].get("page_url", "")
                hit_dict["score"] = hit["_score"]

                hit_list.append(hit_dict)

            result = {
                "page": page,
                "searchCostTime": search_cost_time,
                "totalNums": total_nums,
                "pageNums": page_nums,
                "hitList": hit_list,
            }
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchSuggest(APIView):
    '''
    根据输入返回搜索建议的接口
    '''
    permission_classes = [AllowAny]

    input = openapi.Parameter('input',
                              openapi.IN_QUERY,
                              description="输入文本",
                              type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[input], responses={200: []})
    def get(self, request):
        input_text = request.query_params.get("input", "")
        suggest_list = []
        if input_text:
            s_ = BlogsIndex.search()
            s = s_.suggest('my_suggest',
                           input_text,
                           completion={
                               "field": "suggest",
                               "fuzzy": {
                                   "fuzziness": 2
                               },
                               "size": 8
                           })
            suggestions = s.execute()
            name_set = OrderedSet()
            for match in suggestions.suggest.my_suggest[0].options[:10]:
                source = match._source
                name_set.add(source["title"])
            for name in name_set:
                suggest_list.append(name)
        return Response(suggest_list, status=status.HTTP_200_OK)
