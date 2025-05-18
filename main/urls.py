from django.urls import path
from .views import *
from . import views


app_name = "main"


urlpatterns = [
    path('', mainpage, name="mainpage"),
    path('second', secondpage, name="secondpage"),
    path('new-post', new_post, name="new-post"),
    path('create', create, name="create"),
    path('detail/<int:id>/', detail, name="detail"),
    path('edit/<int:id>', edit, name="edit"),
    path('update/<int:id>', update, name="update"),
    path('delete/<int:id>/', delete, name="delete"),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('tag-list', tag_list, name="tag-list"),
    path('tag-posts/<int:tag_id>', tag_posts, name="tag-posts"),
]