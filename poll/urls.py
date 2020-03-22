from django.urls import path,include
from poll.views import *

urlpatterns = [
    path('add/', PollView.as_view(), name='poll_add'),
    path('<int:id>/edit/', PollView.as_view(), name='poll_edit'),
    path('<int:id>/delete/', PollView.as_view(), name='poll_delete'),
    path('',index,name='index'),
    path('<int:id>/details',details,name='details'),
    path('<int:id>/',poll,name='poll'),

]