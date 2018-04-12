from django.conf.urls import url

from .views import UserCenterInfoView

urlpatterns=[
    url(r'info/',UserCenterInfoView.as_view(),name='info'),
]