from django.conf.urls import url
from . import views
from django.urls import path


app_name = 'blog'
urlpatterns = [

    url(r'^$', views.abc, name='abc'),
   # url(r'^accounts/profile/$', views.abc, name='abc'),

    url(r'^home/$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/success/$', views.register_success, name='success'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^search_pharmacies/$', views.maps, name='maps'),
    url(r'^search/$', views.search, name='search'),
    url(r'^home2/$', views.home2, name='home2'),
    path(' ', views.product_list, name='product_list'),
	path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
	path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search_medicine', views.search_medicine, name='search_medicine'),
    path('medicine_detail/<str:med_name>/', views.medicine_detail, name='medicine_detail'),

]

