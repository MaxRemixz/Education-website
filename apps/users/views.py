from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
# Q 可以完成并集
from django.db.models import Q

from .models import UserProfile


class CustomBackend(ModelBackend):
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username)|Q(email=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None


def user_login(request):
	if request.method == "POST":
		user_name = request.POST.get("username", "")
		pass_word = request.POST.get("password", "")
		print(user_name)
		print(pass_word)
		# authenticate 是将用户名和密码提交到数据库发起验证。验证是否正确
		# 实际的登录是用login方法
		user = authenticate(username=user_name, password=pass_word)
		if user is not None:
			login(request, user)
			return render(request, "index.html")
		else:
			return render(request, "login.html", {"msg":"用户名或密码错误!"})
	elif request.method == "GET":
		return render(request, "login.html", {})