from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('category', views.category, name='category'),
    path('like/<slug:slug>', views.LikePost.as_view(), name='like_post')
]
