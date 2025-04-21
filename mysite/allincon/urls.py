from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'), #polls/ 이후 아무것도 작성안하면 polls의 views객체의 index함수 실행한다는 의미
]