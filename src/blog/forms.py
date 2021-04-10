from django.forms import (Form, ModelForm, CharField, EmailField,
                          TextInput, Textarea, EmailInput, widgets)
from blog.models import Comment


# переменные для дальнейшего использования в коде
attrs = {'class': 'form-control'}
email_widget = EmailInput(attrs=attrs)
textarea_widget = Textarea(attrs=attrs)
# ------------------------------------------------


# Формы
class EmailPostForm(Form):

    # name = CharField(max_length=100, widget=TextInput(attrs=attrs))
    email = EmailField(required=True, widget=email_widget, label='Ваш email')
    to = EmailField(required=True, widget=email_widget, label='Кому вы хотите отправить')
    comments = CharField(required=False, widget=textarea_widget, label='Комментарии')



class CommentForm(ModelForm):

    class Meta:
        # model = 'blog.Comment'
        model = Comment
        fields = 'name', 'email', 'body',
        widgets = {
            'name': TextInput(attrs=attrs),
            'email': email_widget,
            'body': textarea_widget,
        }
        labels = {
            'name': 'Ваше имя',
            'email': 'Ваша почта',
            'body': 'Комментарий',
        }


class SearchForm(Form):

    query = CharField(required=False, widget=TextInput(attrs=attrs))
