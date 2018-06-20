from __future__ import absolute_import

from celery.task import Task
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

from config.celery import app
from member.models import User, InviteUser, PointHistory
from utils.tokengenerator import account_activation_token, invite_token


class SignupEmailTask(Task):
    def run(self, pk):
        # 이메일 발송
        mail_subject = 'byCAL 이메일 인증.'
        user = User.objects.filter(pk=pk).get()
        message = render_to_string('singup_activation.html', {
            'user': user.nickname,
            'domain': 'bycal.co',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.username
        email = EmailMultiAlternatives(
            mail_subject, to=[to_email]
        )
        email.attach_alternative(message, "text/html")
        email.send()
        # if email.send():
        #     return True
        # return False


class PasswordResetTask(Task):
    # 이메일 발송
    def run(self, pk):
        user = User.objects.filter(pk=pk).get()

        mail_subject = 'byCAL 비밀번호 변경.'
        message = render_to_string('pw_change.html', {
            'user': user,
            'domain': 'bycal.co',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.username
        email = EmailMultiAlternatives(
            mail_subject, to=[to_email]
        )
        email.attach_alternative(message, "text/html")
        email.send()


class InviteUserTask(Task):
    def run(self, user_pk, send_user_pk):
        user = InviteUser.objects.filter(pk=user_pk).get()
        send_user = User.objects.filter(pk=send_user_pk).get()
        # 이메일 발송
        mail_subject = 'byCAL Invite'
        message = render_to_string('invitation.html', {
            'user': user,
            'domain': 'bycal.com',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': invite_token.make_token(user),
            'send_user': send_user.nickname
        })
        to_email = user.email
        email = EmailMultiAlternatives(
            mail_subject, to=[to_email]
        )
        email.attach_alternative(message, "text/html")
        email.send()


#
class MemberPointTask(Task):
    def run(self, point, message):
        all_member = User.objects.all()
        for i in all_member:
            i.point += int(point)
            PointHistory.objects.reward(user=i, point=point, history=message)

        return True


app.tasks.register(SignupEmailTask)
app.tasks.register(PasswordResetTask)
app.tasks.register(InviteUserTask)
app.tasks.register(MemberPointTask)