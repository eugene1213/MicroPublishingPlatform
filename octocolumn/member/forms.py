from distutils import errors

from django import forms

from column.models import PreAuthorPost, Post
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


class AuthorIsActive(forms.Form):
    def form_action(self, author_post):
        user = author_post.author
        author = Author.objects.filter(author=user).get()
        post = PreAuthorPost.objects.filter(author=author_post.author).all()
        if post is not None:
            for i in post:
                Post.objects.create(author=i.author, main_content=i.main_content, price=i.price, preview=i.preview,
                                    title=i.title, cover_image=i.cover_image)
        author.is_active = True
        author.save()
        return PreAuthorPost.objects.filter(author=author_post.author).all().delete()

    def save(self, author_post):
        author = self.form_action(author_post)
        print(author_post)
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