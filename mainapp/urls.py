from django.urls import path
from mainapp import views

mainpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('update', views.UpdateVideo.as_view(), name="update"),
    path('navigation', views.Navigation.as_view(), name="navigation"),

    path('process/<str:video_name>', views.Process.as_view(), name="process"),
    path('topic', views.Topic.as_view(), name="topic"),
    path('anchor', views.Anchor.as_view(), name="anchor"),

    path('delete', views.DeleteVideo.as_view(), name="delete")

]
