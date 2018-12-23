from django.shortcuts import render
from django.views.generic import View

from .models import CourseOrg, CityDict


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        return render(request, 'org-list.html', {
            "all_orgs": all_orgs,
            "all_citys": all_citys,
        })