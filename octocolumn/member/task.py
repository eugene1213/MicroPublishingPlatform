from __future__ import absolute_import

from celery.task import Task
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

from config.celery import app
from member.models import User
from utils.tokengenerator import account_activation_token


class SignupEmailTask(Task):
    def run(self, pk):
        # 이메일 발송
        mail_subject = 'Octocolumn 이메일 인증.'
        user = User.objects.filter(pk=pk).get()
        message = render_to_string('singup_activation.html', {
            'user': user.nickname,
            'domain': 'www.octocolumn.com',
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


app.tasks.register(SignupEmailTask)