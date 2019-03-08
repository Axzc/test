from apps.goods.views import IndexView, ArticleDetailsView
from django.conf.urls import  url


urlpatterns = [
    url(r'^detail/(?P<aricle_id>\d+)$', ArticleDetailsView.as_view(), name='detail'),
    url(r'^', IndexView.as_view(), name='index'),

]