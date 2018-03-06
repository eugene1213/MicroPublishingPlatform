import collections
import re

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from member.models import User


class PostPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        p = '^http:'

        next_i = self.get_next_link()
        if next_i is None:
            next_url = None
        else:
            next_url = re.sub(p, 'https:', next_i)

        previous_i = self.get_previous_link()
        if previous_i is None:
            previous_url = None
        else:
            previous_url = re.sub(p, 'https:', previous_i)

        list = []
        for i in data:
            user = User.objects.filter(pk=i['author']).get()
            data = {
                "author": user.last_name + ' ' + user.first_name,
                "content": i['content'],
                "created_date": i['created_date'],
                "parent_id": i['parent_id']

            }
            list.append(data)

        ret = collections.OrderedDict()
        ret["count"] = self.page.paginator.count
        ret["next"] = next_url
        ret["previous"] = previous_url
        ret["results"] = list
        return Response(ret)