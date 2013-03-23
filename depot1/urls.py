from django.conf.urls.defaults import *
from models import *
from views import *
from tastypie.api import Api
from depot1.api import LineItemResource
from django.views.generic.simple import direct_to_template

v1_api = Api(api_name='v1')
v1_api.register(LineItemResource())

urlpatterns = patterns('',
    (r'^store/$', store_view),
    (r'^create/$', create_product),
    (r'^list/$', list_product ),
    (r'^delete/(?P<id>\d+)/$', delete_product),
    (r'^edit/(?P<id>\d+)/$', edit_product),
    (r'^view/(?P<id>\d+)/$', view_product),
    (r'upload_image/$', upload_image),
    (r'^cart/view/$', view_cart),
    (r'^cart/view/(?P<id>\d+)/$', add_to_cart),
    (r'^cart/clean/$', clean_cart),
    (r'^create/order/$', create_order),
    (r'^api/', include(v1_api.urls)),
    (r'^about/$', direct_to_template, {'template': 'about.html'}),
)