from django.forms import Form, CharField, EmailField, TextInput, Textarea, EmailInput, widgets


attrs = {'class': 'form-control'}

email_widget = EmailInput(attrs=attrs)

class EmailPostForm(Form):

    name = CharField(max_length=100, widget=TextInput(attrs=attrs))
    email = EmailField(required=True, widget=email_widget)
    to = EmailField(required=True, widget=email_widget)
    comments = CharField(required=False, widget=Textarea(attrs=attrs))
