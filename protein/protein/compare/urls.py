from django.conf.urls import url
from . import views

app_name = 'compare'

urlpatterns = [

    #/compare/
    url(r'^$', views.index, name='index'),

    #/compare/display/
    url(r'^display/$', views.display, name='display'),

    #/compare/display1/
    url(r'^display1/$', views.display_1, name='display_1'),

    #/compare/display2/
    url(r'^display2/$', views.display_2, name='display_2'),

    #/compare/display3/
    url(r'^display3/$', views.display_3, name='display_3'),
]
