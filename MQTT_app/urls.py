from django.urls import path
from . import views

urlpatterns = [
    #path('', views.weather, name='post_list'),
    path('', views.start_FWI, name='post_list'),
    
    #path('publish', views.publish_message, name='publish'),
    path('UPdate', views.start_mqtt, name='update'),
    path('start_wfi', views.start_FWI, name='start_wfi'),
    path('getTemp',views.getTemp,name='getTemp'),
    path('update_weather', views.update_weather, name='update_weather'),
]