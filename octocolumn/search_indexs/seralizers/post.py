# from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
# from rest_framework import serializers
#
# from search_indexs.document.post import PostDocument
#
#
# class PostDocumentSerializer(DocumentSerializer):
#     pk = serializers.IntegerField(read_only=True)
#
#     title = serializers.CharField(read_only=True)
#     author = serializers.CharField(read_only=True)
#     price = serializers.IntegerField(read_only=True)
#     created_date = serializers.DateTimeField(read_only=True)
#
#     class Meta(object):
#
#         # Specify the correspondent document class
#         document = PostDocument
#
#         # List the serializer fields. Note, that the order of the fields
#         # is preserved in the ViewSet.
#         fields = (
#             'pk',
#             'title',
#             'author',
#             'created_date',
#             'price',
#             # 'tags',
#         )
