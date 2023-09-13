from django.urls import path
from . import views


app_name  = 'user_servcies'

urlpatterns = [
    path("",views.common_user.as_view()),
    path("<int:pk>",views.users.as_view()),
    path("login",views.login_user,name="login"),
    path("logout",views.logout_user,name="logout"),
    path("commuter",views.Commuter.as_view()),
    path("commuter/<int:pk>",views.Commuters.as_view()),
    path("driver",views.driver.as_view()),
    path("driver/<int:pk>",views.drivers.as_view()),
    path("admin",views.Admin.as_view()),
    path("admin/<int:pk>",views.Admins.as_view()),
    path("admin/<str:name>/<str:pk>",views.custom_admin.as_view())
    
    
]
# baseUrl/commuter/userId
# baseUrl/userId {first_name,contact,email}

# baseUrl/user/admin/commuter/admincode