from django.db import models

__all__ = (
    'Tag',
    'SearchTag',
)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag({})'.format(self.name)


class SearchTag(models.Model):
    post = models.ForeignKey('column.Post')
    tag = models.CharField(max_length=255)

    def __str__(self):
        return 'Post({}), Tag({})'.format(self.post, self.name)
