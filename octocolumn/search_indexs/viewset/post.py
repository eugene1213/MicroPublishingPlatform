# from django_elasticsearch_dsl_drf.constants import (
#     LOOKUP_FILTER_TERMS,
#     LOOKUP_FILTER_RANGE,
#     LOOKUP_FILTER_PREFIX,
#     LOOKUP_FILTER_WILDCARD,
#     LOOKUP_QUERY_IN,
#     LOOKUP_QUERY_GT,
#     LOOKUP_QUERY_GTE,
#     LOOKUP_QUERY_LT,
#     LOOKUP_QUERY_LTE,
#     LOOKUP_QUERY_EXCLUDE,
# )
# from django_elasticsearch_dsl_drf.filter_backends import (
#     FilteringFilterBackend,
#     IdsFilterBackend,
#     OrderingFilterBackend,
#     DefaultOrderingFilterBackend,
#     SearchFilterBackend,
# )
# from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
# from rest_framework.pagination import PageNumberPagination
#
# from search_indexs.document.post import PostDocument
# from search_indexs.seralizers.post import PostDocumentSerializer
#
#
# class PostDocumentView(DocumentViewSet):
#
#     document = PostDocument
#     serializer_class = PostDocumentSerializer
#     pagination_class = PageNumberPagination
#
#     lookup_field = 'pk'
#     filter_backends = [
#         FilteringFilterBackend,
#         IdsFilterBackend,
#         OrderingFilterBackend,
#         DefaultOrderingFilterBackend,
#         SearchFilterBackend,
#     ]
#     # Define search fields
#     search_fields = (
#         'title',
#         'author',
#     )
#     # Define filter fields
#     filter_fields = {
#         # 'id': {
#         #     'field': 'id',
#         #     # Note, that we limit the lookups of id field in this example,
#         #     # to `range`, `in`, `gt`, `gte`, `lt` and `lte` filters.
#         #     'lookups': [
#         #         LOOKUP_FILTER_RANGE,
#         #         LOOKUP_QUERY_IN,
#         #         LOOKUP_QUERY_GT,
#         #         LOOKUP_QUERY_GTE,
#         #         LOOKUP_QUERY_LT,
#         #         LOOKUP_QUERY_LTE,
#         #     ],
#         # },
#         'title': 'title.raw',
#         'author': 'author.raw',
#         'created_date': 'created_date',
#         'price': {
#             'field': 'price.raw',
#             # Note, that we limit the lookups of `price` field in this
#             # example, to `range`, `gt`, `gte`, `lt` and `lte` filters.
#             'lookups': [
#                 LOOKUP_FILTER_RANGE,
#                 LOOKUP_QUERY_GT,
#                 LOOKUP_QUERY_GTE,
#                 LOOKUP_QUERY_LT,
#                 LOOKUP_QUERY_LTE,
#             ],
#         },
#
#         # 'tags': {
#         #     'field': 'tags',
#         #     # Note, that we limit the lookups of `tags` field in
#         #     # this example, to `terms, `prefix`, `wildcard`, `in` and
#         #     # `exclude` filters.
#         #     'lookups': [
#         #         LOOKUP_FILTER_TERMS,
#         #         LOOKUP_FILTER_PREFIX,
#         #         LOOKUP_FILTER_WILDCARD,
#         #         LOOKUP_QUERY_IN,
#         #         LOOKUP_QUERY_EXCLUDE,
#         #     ],
#         # },
#         # 'tags.raw': {
#         #     'field': 'tags.raw',
#         #     # Note, that we limit the lookups of `tags.raw` field in
#         #     # this example, to `terms, `prefix`, `wildcard`, `in` and
#         #     # `exclude` filters.
#         #     'lookups': [
#         #         LOOKUP_FILTER_TERMS,
#         #         LOOKUP_FILTER_PREFIX,
#         #         LOOKUP_FILTER_WILDCARD,
#         #         LOOKUP_QUERY_IN,
#         #         LOOKUP_QUERY_EXCLUDE,
#         #     ],
#         # },
#     }
#     # Define ordering fields
#     ordering_fields = {
#         'title': 'title.raw',
#         'price': 'price.raw',
#         'created_date': 'created_date',
#     }
#     # Specify default ordering
#     ordering = ('title', 'price')
