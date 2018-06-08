# from django.conf import settings
# from django_elasticsearch_dsl import DocType, Index, fields
# from elasticsearch_dsl import analyzer
#
# from column.models import Post
#
#
# INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
#
# INDEX.settings(
#     number_of_shards=1,
#     number_of_replicas=1
# )
#
# html_strip = analyzer(
#     'html_strip',
#     tokenizer="standard",
#     filter=["standard", "lowercase", "stop", "snowball"],
#     char_filter=["html_strip"]
# )
#
# @INDEX.doc_type
# class PostDocument(DocType):
#     title = fields.StringField(
#         analyzer=html_strip,
#         fields={
#             'raw': fields.StringField(analyzer='keyword'),
#         }
#     )
#
#     author = fields.StringField(
#         attr='author_indexing',
#         analyzer=html_strip,
#         fields={
#             'raw': fields.StringField(analyzer='keyword'),
#         }
#     )
#
#     created_date = fields.DateField()
#
#     price = fields.IntegerField()
#
#     class Meta(object):
#
#         model = Post  # The model associate with this DocType