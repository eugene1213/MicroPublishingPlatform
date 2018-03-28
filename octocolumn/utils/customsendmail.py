from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from utils.tokengenerator import account_activation_token, invite_token


# 회원가입 인증 메일
def signup_email_send(user):
    # 이메일 발송
    mail_subject = 'Octocolumn 이메일 인증.'
    # urlrequest = request
    # url = get_current_site(urlrequest)
    message = render_to_string('singup_activation.html', {
        'user': user,
        'domain': 'www.octocolumn.com',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.username
    email = EmailMultiAlternatives(
        mail_subject, to=[to_email]
    )
    email.attach_alternative(message, "text/html")
    if not email.send():
        return False
    return True


# 패스워드 초기화
def password_reset_email_send(user):
    # 이메일 발송
    mail_subject = 'Octocolumn 비밀번호 변경.'
    message = render_to_string('pw_change.html', {
        'user': user,
        'domain': 'localhost:8000',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.username
    email = EmailMultiAlternatives(
        mail_subject, to=[to_email]
    )
    email.attach_alternative(message, "text/html")
    if not email.send():
        return False
    return True


# 초대 메일
def invite_email_send(user, send_user):
    # 이메일 발송
    mail_subject = 'Octocolumn Invite'
    message = render_to_string('invitation.html', {
        'user': user,
        'domain': 'www.octocolumn.com',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': invite_token.make_token(user),
        'send_user': send_user
    })
    to_email = user.email
    email = EmailMultiAlternatives(
        mail_subject, to=[to_email]
    )
    email.attach_alternative(message, "text/html")
    if not email.send():
        return False
    return True