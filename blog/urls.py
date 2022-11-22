""" URLs imports to link each blog functionality """

from django.urls import path
from . import views
from .views import CommentUpdateView, CommentDeleteView


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('category/<int:id>', views.category, name='category'),
    path('like/<slug:slug>', views.LikePost.as_view(), name='like_post'),
    path('update_comment/<int:pk>', CommentUpdateView.as_view(), name='update_comment'),
    path('delete_comment/<int:pk>', CommentDeleteView.as_view(), name='delete_comment'),
]
