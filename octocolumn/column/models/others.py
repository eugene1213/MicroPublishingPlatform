from django.db import models

__all__ = (
    # 'Tag',
    'SearchTag',
    'PreSearchTag',
    # 'Recommend'
)

#
# class Tag(models.Model):
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return 'Tag({})'.format(self.name)


class SearchTag(models.Model):
    post = models.ForeignKey('column.Post')
    tag = models.CharField(max_length=255)

    def __str__(self):
        return 'Post({}), Tag({})'.format(self.post, self.tag)

    # @property
    # def tags_indexing(self):
    #     if self.tag is not None:
    #         for i in self.tag:
    #         return [tag.title for tag in self.tag]


class PreSearchTag(models.Model):
    post = models.ForeignKey('column.PreAuthorPost')
    tag = models.CharField(max_length=255)

    def __str__(self):
        return 'Post({}), Tag({})'.format(self.post, self.tag)


# class Recommend(models.Model):
#     text = models.CharField(max_length=255)
#
#     def __str__(self):
#         return 'Tag({})'.format(self.text)