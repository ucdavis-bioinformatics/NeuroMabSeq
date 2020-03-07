from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.main_page, name='main page'),
    path('query/', views.EntryListView, name='sequence_query'),
    path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='sequence_entry'),

]