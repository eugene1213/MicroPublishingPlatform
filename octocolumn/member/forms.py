from distutils import errors

from django import forms
from django.contrib.admin.helpers import ActionForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from column.models import PreAuthorPost, Post, Temp, PreSearchTag, SearchTag, PostStar, Tag, Recommend
from member.models import Author
# from common.utils import send_email
# from . import errors
# class AccountActionForm(forms.Form):
#     comment = forms.CharField(
#         required=False,
#         widget=forms.Textarea,
#     )
#     send_email = forms.BooleanField(
#         required=False,
#     )
#     @property
#     def email_subject_template(self):
#         return 'email/account/notification_subject.txt'
#     @property
#     def email_body_template(self):
#         raise NotImplementedError()
#     def form_action(self, account, user):
#         raise NotImplementedError()
#     def save(self, account, user):
#         try:
#             account, action = self.form_action(account, user)
#         except errors.Error as e:
#             error_message = str(e)
#             self.add_error(None, error_message)
#             raise
#         if self.cleaned_data.get('send_email', False):
#             send_email(
#                 to=[account.user.email],
#                 subject_template=self.email_subject_template,
#                 body_template=self.email_body_template,
#                 context={
#                     "account": account,
#                     "action": action,
#                 }
#             )
#     return account, action
#
from member.task import IsActiveAuthorMail


class AuthorIsActive(forms.Form):
    def form_action(self, author_post):

        user = author_post.author
        author = Author.objects.filter(author=user).get()

        # if user:
        #     mail_subject = 'byCAL 출판 완료.'
        #     user = user
        #     message = render_to_string('accept.html', {
        #         'user': user.nickname,
        #     })
        #     to_email = user.username
        #     email = EmailMultiAlternatives(
        #         mail_subject, to=[to_email]
        #     )
        #     email.attach_alternative(message, "text/html")
        #     email.send()
        #     pass

        if user:
            task = IsActiveAuthorMail
            if task.delay(user.pk):
                post = PreAuthorPost.objects.filter(author=author_post.author).all()
                if post is not None:
                    for i in post:
                        new_post = Post.objects.select_related('author').create(
                            author=i.author,
                            main_content=i.main_content,
                            price=i.price,
                            preview=i.preview,
                            title=i.title,
                            cover_image=i.cover_image,
                            thumbnail=i.thumbnail,

                        )
                        PostStar.objects.create(post=new_post)
                        tag = i.tags.all()
                        for j in tag:
                            tags = Tag.objects.create(tags=j.tags)
                            new_post.tags.add(tags)


                        recommend = i.recommend.all()
                        for k in recommend:
                            recommeds = Recommend.objects.create(text=k.text)
                            new_post.recommend.add(recommeds)
                    author.is_active = True
                    author.save()
                    return PreAuthorPost.objects.filter(author=author_post.author).all().delete()
                raise ValueError
            raise ValueError
        raise ValueError

    def save(self, author_post):
        author = self.form_action(author_post)
        if author:
            return author
        raise ValueError("error")


class PostDraftAction(forms.Form):
    def form_action(self, author_post):

        user = author_post.author
        author = Author.objects.filter(author=user).get()

        post = PreAuthorPost.objects.filter(author=author_post.author).all()
        if post is not None:
            for i in post:
                Temp.objects.create(
                    author=i.author,
                    main_content=i.main_content,
                    title=i.title,
                    )

        author.save()
        return PreAuthorPost.objects.filter(author=author_post.author).all().delete()

    def save(self, author_post):
        author = self.form_action(author_post)
        if author:
            return author
        raise ValueError("error")

# amount = forms.IntegerField(
#         min_value=Account.MIN_DEPOSIT,
#         max_value=Account.MAX_DEPOSIT,
#         required=True,
#         help_text=’How much to deposit?’,
#     )
#     reference_type = forms.ChoiceField(
#         required=True,
#         choices=Action.REFERENCE_TYPE_CHOICES,
#     )
#     reference = forms.CharField(
#         required=False,
#     )
#     email_body_template = 'email/account/deposit.txt'
#     field_order = (
#         'amount',
#         'reference_type',
#         'reference',
#         'comment',
#         'send_email',
#     )


class PointRewardForm(ActionForm):
    point = forms.IntegerField()
    message = forms.CharField()

    # def form_action(self, point):
    #     pass
