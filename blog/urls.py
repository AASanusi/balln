from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('category/<int:id>', views.category, name='category'),
    path('like/<slug:slug>', views.LikePost.as_view(), name='like_post'),
    path('update_comment/<int:comment_id>', views.EditComment.as_view(), name='update_comment'),
    path('delete_comment/<int:comment_id>', views.DeleteComment.as_view(), name='delete_comment'),
]
