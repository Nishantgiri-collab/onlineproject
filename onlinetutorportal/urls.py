
from django.contrib import admin
from django.urls import path
from tutorapp import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

sitemaps_dict = {
    "static": StaticViewSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registration/', views.register_user, name='registration'),
    path('login/', views.login_user, name='login'),
    path("book/", views.book_class, name="book_class"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps_dict}, name="sitemap"),
]




