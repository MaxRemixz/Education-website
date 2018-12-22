from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    # required=True 代表是必填的字段 字段的名称必须和前端页面form表单的input标签的name属性值相同
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})
