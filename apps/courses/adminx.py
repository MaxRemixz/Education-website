from .models import Course, Lesson, Video, CourseResource, BannerCourse
import xadmin


class LessonInline(object):
	model = Lesson
	extra = 0


class CourseResourceInline(object):
	model = CourseResource
	extra = 0


class CourseAdmin(object):
	list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
	search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
	list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
	ordering = ['-students']
	# readonly_fields是只读字段。exclude是隐藏该字段。两个互相冲突
	readonly_fields = ['click_nums', 'fav_nums']
	# exclude = ['fav_nums']
	inlines = [LessonInline, CourseResourceInline]

	def queryset(self):
		qs = super(CourseAdmin, self).queryset()
		qs = qs.filter(is_banner=False)
		return qs


class BannerCourseAdmin(object):
	list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
	search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
	list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
	ordering = ['-students']
	# readonly_fields是只读字段。exclude是隐藏该字段。两个互相冲突
	readonly_fields = ['click_nums', 'fav_nums']
	# exclude = ['fav_nums']
	inlines = [LessonInline, CourseResourceInline]


	def queryset(self):
		qs = super(BannerCourseAdmin, self).queryset()
		qs = qs.filter(is_banner=True)
		return qs


class LessonAdmin(object):
	list_display = ['course', 'name', 'add_time']
	search_fields = ['course', 'name']
	list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
	list_display = ['lesson', 'name', 'add_time']
	search_fields = ['lesson', 'name']
	list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
	list_display = ['course', 'name', 'download', 'add_time']
	search_fields = ['course', 'name', 'download']
	list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)