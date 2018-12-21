from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
# Q 可以完成并集
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile
from .forms import LoginForm, RegisterForm
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
	def authenticate(self, username=None, password=None, **kwargs):
		try:
			user = UserProfile.objects.get(Q(username=username)|Q(email=username))
			if user.check_password(password):
				return user
		except Exception as e:
			return None


class RegisterView(View):
	def get(self, request):
		register_form = RegisterForm()
		return render(request, "register.html", {'register_form': register_form})
	def post(self, request):
		register_form = RegisterForm(request.POST)
		if register_form.is_valid():
			user_name = request.POST.get("email", "")
			pass_word = request.POST.get("password", "")
			user_profile = UserProfile()
			user_profile.username = user_name
			user_profile.email = user_name
			user_profile.password = make_password(pass_word)
			user_profile.is_active = False
			user_profile.save()
			send_register_email(user_name, "register")
			return render(request, "login.html")
		else:
			return render(request, "register.html", {'register_form': register_form})


class LoginView(View):
	def get(self, request):
		return render(request, "login.html", {})
	def post(self, request):
		login_form = LoginForm(request.POST)
		# is_valid 其实就是验证这个login_form实例里面的_errors私有属性是否为空
		# 如果为空。就是没有错误信息。那么就是验证成功
		if login_form.is_valid():
			user_name = request.POST.get("username", "")
			pass_word = request.POST.get("password", "")
			# authenticate 是将用户名和密码提交到数据库发起验证。验证是否正确
			# 实际的登录是用login方法
			user = authenticate(username=user_name, password=pass_word)
			if user is not None:
				login(request, user)
				return render(request, "index.html")
			else:
				return render(request, "login.html", {"msg":"用户名或密码错误!"})
		else:
			return render(request, "login.html", {"login_form":login_form})


# 基于函数的认证方法
# def user_login(request):
# 	if request.method == "POST":
# 		user_name = request.POST.get("username", "")
# 		pass_word = request.POST.get("password", "")
# 		print(user_name)
# 		print(pass_word)
# 		# authenticate 是将用户名和密码提交到数据库发起验证。验证是否正确
# 		# 实际的登录是用login方法
# 		user = authenticate(username=user_name, password=pass_word)
# 		if user is not None:
# 			login(request, user)
# 			return render(request, "index.html")
# 		else:
# 			return render(request, "login.html", {"msg":"用户名或密码错误!"})
# 	elif request.method == "GET":
# 		return render(request, "login.html", {})