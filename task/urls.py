from django.urls import path

from task import views

urlpatterns = [
    path('',views.user_login),
    path('register',views.register),
    path('logout',views.user_logout),
    path('addtask',views.AddTask),
    path('viewtask',views.ViewTask),
    path('status/<int:id>',views.TaskStatus),
    path('delete/<int:id>',views.DeleteTask),
    path('completed',views.CompletedTask),
    path('detailed/<int:id>',views.DetailedView),
    path('edit/<int:id>',views.Edit),
    path('edit/update/<int:id>',views.Update),
    path('forgotpass', views.Forgot_password),
    path('verifypass', views.reset_password),
    path('dashboard',views.Dashboard),
    path('profile',views.CreateProfile),
    path('viewpro',views.ViewProfile),
    path('editpro',views.EditProfile),
    path('changepass',views.Change_password)


]