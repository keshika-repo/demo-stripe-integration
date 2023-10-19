from .views import webhooks
from app.views import UserView,LoginView,TaskView,Userview,AdminView,PaymentAPI
from django.urls import path

urlpatterns = [
    path('register/',UserView.as_view()),
    path('updateuser/<int:id>/',UserView.as_view()),
    path('login/',LoginView.as_view()),
    path('task/',TaskView.as_view()),
    path('task/<int:id>/',TaskView.as_view()),
    path('viewtoken/',Userview.as_view()),
    path('userall/',AdminView.as_view()),
     path('payment/',PaymentAPI.as_view()),
    path('webhook/',view=webhooks)

  
       
]
