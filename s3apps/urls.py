from django.urls import path
from s3apps import views


urlpatterns = [
    path('regions/', views.regions, name='regions'),
    path('get_clusters/', views.get_clusters, name='get_clusters')
]
