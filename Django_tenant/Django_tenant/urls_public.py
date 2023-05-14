from django.contrib import admin
from django.urls import path, include
from sharedapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sharedapp.urls')),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
print("==========public_url=======================", urlpatterns)