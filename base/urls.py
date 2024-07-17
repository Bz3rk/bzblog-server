from django.urls import path
from base.views import ClientRegister, ClientLogin, BlogCreateView, BlogDetailView, BlogListView, TopicListView, BlogDeleteView, BlogUpdateView


urlpatterns = [
    path('register/', ClientRegister, name='register' ),
    path('login/', ClientLogin, name='login' ),
    path('blog-create/', BlogCreateView.as_view(), name='blog-create' ),
    path('blog-detail/<str:pk>', BlogDetailView.as_view(), name='blog-detail' ),
    path('blog-update/<str:pk>', BlogUpdateView.as_view(), name='blog-update' ),
    path('blog-delete/<str:pk>', BlogDeleteView.as_view(), name='blog-delete' ),
    path('blog-list/', BlogListView.as_view(), name='blog-list' ),
    path('topic-list/', TopicListView.as_view(), name='topic-list' ),
]