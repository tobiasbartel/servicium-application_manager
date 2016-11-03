__author__ = 'tbartel'
from django.conf.urls import url
from views import *


app_name = 'module'
urlpatterns = [
    url(r'^(?P<module_name>[\w-]+)/$', module_detail, name='module-detail'),
    url(r'^all/graph/$', all_module_graph),
    url(r'^(?P<my_module_name>[\w-]+)/graph/$', module_graph),
    url(r'^(?P<my_module_name>[\w]+)/(?P<my_payment_method_name>[a-z-,]+)/graph/$', module_graph),
    url(r'^(?P<my_module_name>[\w]+)/(?P<my_payment_method_name>[a-z-,]+)/graph/raw/$', module_graph ),
    url(r'^$', module_overview),
]