from django.conf.urls import url
from django.views.generic import TemplateView

from compare import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='general/compare.html')),
    url(r'^display/$', views.display, name='display'),
    url(r'^display1/$', views.display_1, name='display_1'),
    url(r'^display2/$', views.display_2, name='display_2'),
    url(r'^display3/$', views.display_3, name='display_3'),
]
