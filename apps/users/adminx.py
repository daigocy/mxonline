# -*- encoding:utf-8 -*-
import xadmin
from xadmin import views

from .models import Banner


class BaseSetting(object):
    pass
    # enable_themes = True
    # use_bootswatch = True

xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    site_title = u'慕学网后台管理'
    site_footer = 'mxonline'
    # menu_style = 'accordion'

xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)


class BannerXadmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(Banner, BannerXadmin)



