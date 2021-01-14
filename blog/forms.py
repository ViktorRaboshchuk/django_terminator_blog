from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.forms import UserCreationForm

from blog.models import Comment, Post, Profile


class CommentForm(forms.ModelForm):
    READONLY_FIELDS = ('name', 'email')

    def __init__(self, *args, **kwargs):
        self.readonly_form = kwargs.pop('readonly_form')
        self.request = kwargs.pop("request")
        super(CommentForm, self).__init__(*args, **kwargs)
        if self.request.user.is_authenticated:
            self.fields['name'].initial = self.request.user.username
            self.fields['email'].initial = self.request.user.email

        if self.readonly_form:
            for field in self.READONLY_FIELDS:
                self.fields[field].widget.attrs['readonly'] = True

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user', 'email','first_name','last_name')


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','password1','password2')
