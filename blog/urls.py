from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:category_slug><slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/', views.Category.as_view(), name='category'),
    path('like/<slug:slug>', views.LikePost.as_view(), name='like_post')
]
