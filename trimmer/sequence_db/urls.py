from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('login/', views.LoginView, name='login'),
    path('', views.main_page, name='main page'),
    path('query/', views.EntryListView, name='sequence_query'),
    path('new_query/', views.TrimmerEntryListView, name='sequence_query'),
    path('status/', views.TrimmerStatusListView, name='status'),
    path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='sequence_entry'),
    path('new_entry/<int:pk>/', views.TrimmerEntryDetailView.as_view(), name='sequence_entry'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('api/entry_list/', views.APIEntryListView.as_view()),
]