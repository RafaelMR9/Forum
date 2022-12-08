from django.urls import path
from django.urls.conf import include
from . import views

app_name = 'forum'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.index.as_view()),
    path('registrar', views.SignUpView.as_view(), name='user-register'),
    path('topicos', views.TopicListView.as_view(), name='topics-list'),
    path('topicos/<int:pk>', views.TopicDetailView.as_view(), name='topics-detail'),
    path('topicos/atualiza/<int:pk>', views.TopicUpdateView.as_view(), name='topics-update'),
    path('topicos/cria', views.TopicCreateView.as_view(), name='topics-register')
]
