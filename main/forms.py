from django import forms
from django.contrib.auth.models import User
import re


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    email = forms.EmailField(label='Email', )
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 6:
            raise forms.ValidationError("用户名至少4位")
        elif len(username) > 50:
            raise forms.ValidationError("用户名太长了")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("该用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("该邮箱已存在")
        else:
            raise forms.ValidationError("请输入有效的邮箱！")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("密码至少6位")
        elif len(password1) > 20:
            raise forms.ValidationError("密码至多20位")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码输入不一致")
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50, help_text='请输入用户名邮箱')
    password = forms.CharField(label='密码', widget=forms.PasswordInput, help_text='请输入密码')

    # Use clean methods to define custom validation rules
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("该邮箱不存在，请注册后重试")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError("该用户名不存在，请注册后重试")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("密码至少6位")
        elif len(password) > 20:
            raise forms.ValidationError("密码至多20位")
        return password
