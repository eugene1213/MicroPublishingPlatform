from celery import Task
from notifications.signals import notify

from column.models import Post
from member.models import User
from member.models.user import Relation


class PostCreateNotifySend(Task):
    def run(self, pk, title, post_pk):
        # 이메일 발송
        user = User.objects.filter(pk=pk).get()
        post = Post.objects.filter(pk=post_pk).get()
        follower = Relation.objects.select_related('to_user', 'from_user').filter(to_user=user).all()
        for i in follower:
            notify.send(user, i.from_user, verb=post.title + '이 출판 되었습니다.', target='post@'+ post.pk, description='컬럼')
