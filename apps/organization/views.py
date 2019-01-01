from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite


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
            elif sort == "hot":
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
    """
    用户添加咨询(异步返回数据)
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # commit 为true的话就会直接保存到数据库
            user_ask = userask_form.save(commit=True)
            # 通过异步返回数据给页面(ajax)。不要刷新当前页面
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构详情首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # classname_set 自动内置反向取出数据的方法
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    """
    机构课程列表
    """
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # classname_set 自动内置反向取出数据的方法
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # classname_set 自动内置反向取出数据的方法
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    """
    机构讲师介绍
    """
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # classname_set 自动内置反向取出数据的方法
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'current_page': current_page,
            'course_org': course_org,
            'has_fav': has_fav,
        })


class AddFavView(View):
    """
    用户收藏 和 取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果已经存在 那么就代表用户取消收藏
            exist_records.delete()
            return HttpResponse('{"status": "fail", "msg": "收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = fav_type
                user_fav.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏出错"}', content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表
    """
    def get(self, request):
        all_teacher = Teacher.objects.all()

        # 根据点击量进行排序
        sort = request.GET.get('sort', "")
        if sort == 'hot':
            all_teacher = all_teacher.order_by("-click_nums")

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]

        # 对课程讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 5 代表每一页的数量
        p = Paginator(all_teacher, 5, request=request)
        teachers_count = all_teacher.count()
        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "teachers_count": teachers_count,
            "sort": sort,
            "sorted_teacher": sorted_teacher,
        })