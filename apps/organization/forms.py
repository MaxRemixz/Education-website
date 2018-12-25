from django import forms
from operation.models import UserAsk


# 运用django modelform 可以直接调用save 来存储数据
class UserAskForm(forms.ModelForm):
	class Meta:
		model = UserAsk
		fields = ['name', 'mobile', 'course_name']