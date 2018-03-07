import re
from audioop import reverse

from django.db import models

from member.models import User
from .others import Tag

__all__ = (
    'Comment',
    'CommentLike',
)


class CommentManager(models.Manager):
    def all(self):
        instance = super(CommentManager, self).filter(parent=None)
        return instance


class Comment(models.Model):
    post = models.ForeignKey('column.Post', null=True)
    # 여기서의 author은 post의 author와 전혀무관
    author = models.ForeignKey('member.User', null=True)
    content = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True)
    # html_content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        'member.User',
        through='CommentLike',
        related_name='like_comments',
    )

    objects = CommentManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.make_html_content_and_add_tags()

    def make_html_content_and_add_tags(self):
        # 해시태그에 해당하는 정규표현식
        p = re.compile(r'(#\w+)')
        # findall메서드로 해시태그 문자열들을 가져옴
        tag_name_list = re.findall(p, self.content)
        # 기존 content(Comment내용)을 변수에 할당
        ori_content = self.content
        # 문자열들을 순회하며
        for tag_name in tag_name_list:
            # Tag객체를 가져오거나 생성, 생성여부는 쓰지않는 변수이므로 _처리
            tag, _ = Tag.objects.get_or_create(name=tag_name.replace('#', ''))
            # 기존 content의 내용을 변경
            change_tag = '<a href="{url}" class="hash-tag">{tag_name}</a>'.format(
                # url=reverse('post:hashtag_post_list', args=[tag_name.replace('#', '')]),
                url=reverse('post:hashtag_post_list',
                            kwargs={'tag_name': tag_name.replace('#', '')}),
                tag_name=tag_name
            )
            ori_content = re.sub(r'{}(?![<\w])'.format(tag_name), change_tag, ori_content, count=1)
            # content에 포함된 Tag목록을 자신의 tags필드에 추가
            if not self.tags.filter(pk=tag.pk).exists():
                self.tags.add(tag)
        # 편집이 완료된 문자열을 html_content에 저장
        self.html_content = ori_content
        super().save(update_fields=['html_content'])

    def comment_like_toggle(self, user):
        # 1. 주어진 user가 User객체인지 확인
        #    아니면 raise ValueError()
        # 2. 주어진 user를 follow하고 있으면 해제
        #    안 하고 있으면 follow함
        if not isinstance(user, User):
            raise ValueError('"user" argument must be User instance!')

        comment_like, relation_created = self.like_user_relation.get_or_create(user=user)
        if relation_created:
            return True
        comment_like.delete()
        return False

    def children(self):  # replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


class CommentLike(models.Model):
    comment = models.ForeignKey(
        'Comment',
        null=True,
    )
    user = models.ForeignKey(
        'member.User',
         null=True,
         related_name='like_user_relation',
                             )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('comment', 'user'),
        )