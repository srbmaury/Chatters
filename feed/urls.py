from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, show_profile, LikeView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('create/', PostCreateView.as_view(), name='postcreate'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='postupdate'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='postdelete'),
    path('<str:username>/show_profile/', show_profile, name='show_profile'),
    path('like/<int:pk>/', LikeView, name='like_post'),
]