
from django.contrib import admin
from django.urls import path
from tutorapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registration/', views.register_user, name='registration'),
    path('login/', views.login_user, name='login'),
    path("book/", views.book_class, name="book_class"),
]
