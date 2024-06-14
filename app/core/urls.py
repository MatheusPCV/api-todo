from django.urls import path
from todo.views.taskView import TaskView
from todo.views.userView import UserView
from todo.views.userDeleteView import UserDeleteView
from todo.views.loginUserView import LoginUserView
from todo.views.logoutUserView import LogoutUserView

urlpatterns = [
    path("", LoginUserView.as_view(), name="home"),
    path("tasks/", TaskView.as_view(), name="tasks"),
    path("register/", UserView.as_view(), name="register"),
    path("logout/", LogoutUserView.as_view(), name="logout"),
    path("tasks/<str:id>/", TaskView.as_view(), name="delete-task"),
    path("deleteaccount/", UserDeleteView.as_view(), name="delete-account")
]
