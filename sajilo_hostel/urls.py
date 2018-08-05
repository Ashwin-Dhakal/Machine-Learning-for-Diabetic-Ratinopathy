from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin

from sajilo import views as sajilo_views

urlpatterns = [
    url(r'^$', sajilo_views.index, name='index'), #this is for the homepage
    # url(r'^hostel_list/$', sajilo_views.hostel_list),
    # url(r'^hostel_detail/(?P<id>\d+)/$', sajilo_views.hostel_detail , name = "hostel_detail"),
    url(r'^searchlist/',sajilo_views.searchlist,name='searchlist'),
    url(r'^admin/', admin.site.urls),

    # url(r'^hostel_list/', include('sajilo.urls')),
            ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)