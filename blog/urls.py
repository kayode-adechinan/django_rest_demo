
from blog import views
from django.urls import path

urlpatterns = [
    path('notes/', views.note_list),
    path('notes/<int:note_id>/', views.note_detail),
]
