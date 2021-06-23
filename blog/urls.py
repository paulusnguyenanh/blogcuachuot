from django.urls import path
from blog.views import (
	create_blog_view,
	detail_blog_view,
	edit_blog_view,
    dashboard,
    delete_post,

)

app_name = 'blog'

urlpatterns = [
    path('dashboard/',dashboard, name='dashboard'),
    path('create/', create_blog_view, name="create"),
    path('<slug>/', detail_blog_view, name="detail"),
    path('<slug>/edit/', edit_blog_view, name="edit"),
    path('<slug>/delete/', delete_post, name="delete"),

 ]