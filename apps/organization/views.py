from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserAskForm


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        # 根据点击数取出最热门的三个课程来进行排序
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
        	all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
        	all_orgs = all_orgs.filter(category=category)

        # 学习人数 课程数
        sort = request.GET.get('sort', "")
        if sort:
        	if sort == "students":
        		all_orgs = all_orgs.order_by("-students")
        	elif sort == "courses":
        		all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 5 代表每一页的数量
        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "city_id": city_id,
            "category": category,
            "org_nums": org_nums,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class AddUserAskView(View):
    def get(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # commit 为true的话就会直接保存到数据库
            user_ask = userask_form.save(commit=True)