from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^users(?:/(?P<user_id>[0-9]+))?/$', 
    	staff_user, name='staff_user'),
    url(r'^hardware(?:/(?P<hardware_id>[0-9]+))?/$', 
    	hardware, name='hardware'),
    url(r'^track(?:/(?P<track_id>[0-9]+))?/$', 
    	hardware_track_history, name='hardware_track_history'),
    url(r'^repair(?:/(?P<repair_id>[0-9]+))?/$', 
    	repair_history, name='repair_history'),
    url(r'^user/best', best_employee, name='best_employee' )
]
