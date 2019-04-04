from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from.views import IndexView, FindTripView, BookView, TicketView, DownloadView

app_name = 'home'

urlpatterns = [
    url(r'^booking/success/ticket/download/(?P<pk>\d+)/$', DownloadView.as_view(), name='download'),
    url(r'^booking/success/ticket/(?P<pk>\d+)/$', TicketView.as_view(), name='ticket'),
    url(r'^confirm/(?P<pk>\d+)/$', BookView.as_view(), name='book'),
    url(r'^search/(?P<time>[\w\- ]+)/(?P<start>[\w\- ]+)/(?P<end>[\w\- ]+)/$', FindTripView.as_view(), name='find'),
    url(r'^$', IndexView.as_view(), name='home')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

