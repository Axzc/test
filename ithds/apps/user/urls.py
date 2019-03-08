from apps.user.views import SignupView, ActiveView, LoginView, UserCenterView, LogoutView
from django.contrib.auth.decorators import login_required
from django.conf.urls import url


urlpatterns = [
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 用户激活
    url(r'^homepage$', login_required(UserCenterView.as_view()), name='usercenter')
]
