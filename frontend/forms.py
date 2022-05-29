from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from recipes.models import Recipe, Image, Comment

class AuthForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = ''
        self.fields["password"].label = ''
        self.fields["username"].widget.attrs.update({'id': 'login_email', 'class': 'std', 'name':'username',
                                                     'placeholder': 'Логин'})
        self.fields['password'].widget.attrs.update({'type': 'password', 'id': 'passwdL', 'name': 'password',
                                                     'class': 'account_input', 'value': '', 'placeholder': 'Пароль'})


class RegForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields["username"].widget.attrs.update({'id': 'login_create', 'class': 'std', 'name':'username',
                                                     'placeholder': 'Логин'})
        self.fields["email"].widget.attrs.update({'id': 'email_create', 'class': 'std', 'name':'email',
                                                  'placeholder': 'E-mail'})
        self.fields['password1'].widget.attrs.update({'type': 'password', 'id': 'passwd', 'name': 'password1',
                                                      'class': 'account_input', 'value': '', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'type': 'password', 'id': 'passwd_repeat', 'name': 'password2',
                                                      'class': 'account_input', 'value': '',
                                                      'placeholder': 'Повторить пароль'})

    def save(self, commit=True):
        instance = super(RegForm, self).save(commit=False)
        self.is_valid()
        instance.email = self.cleaned_data['email']
        if commit:
            instance.save()
        return instance


class RecipeForm(forms.ModelForm):
    pathImage = forms.ImageField(required=False)
    title = forms.CharField(max_length=50)
    description = forms.CharField(widget=CKEditorUploadingWidget())
    pathImage.label = 'Изображение блюда'
    title.label = 'Название блюда'
    description.label = 'Описание блюда'

    class Meta:
        model = Recipe
        fields = ['pathImage', 'title', 'description']


class ImageForm(forms.ModelForm):
    pathImage = forms.ImageField()

    class Meta:
        model = Image
        fields = ['pathImage']


class CommentForm(forms.ModelForm):
    data = forms.CharField(widget=forms.Textarea)
    data.label = 'Сообщение'

    data.widget.attrs.update({'class': 'form-control'})
    data.widget.attrs.update(rows=3)

    class Meta:
        model = Comment
        fields = ['data']