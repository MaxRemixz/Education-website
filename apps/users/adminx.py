import xadmin
from .models import EmailVerifyRecord, Banner

class EmailVerifyRecordAdmin(object):
	list_display = ['code', 'email', 'send_type', 'send_time']
	search_fields = ['code', 'email', 'send_type']
	list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
	list_display = ['title', 'url', 'image', 'index', 'add_time']
	search_fields = ['title', 'url', 'image', 'index']
	list_filter = ['title', 'url', 'image', 'index', 'add_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)