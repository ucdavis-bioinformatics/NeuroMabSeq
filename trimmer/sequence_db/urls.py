from django.urls import path, include
from django.conf.urls import url  #, patterns
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('login/', views.LoginView, name='login'),
    path('', views.main_page, name='main page'),
    url(regex=r'^new_query/$', view=views.TrimmerEntryListView, name='sequence_query'),
    path('status/', views.TrimmerStatusListView, name='status'),
    path('faq/', views.faq_view, name='faq'),
    path('blat/', views.blat, name='Blat'),
    path('new_entry/<int:pk>/', views.TrimmerEntryDetailView.as_view(), name='sequence_entry'),
    # path('analytics/', views.analytics_view, name='analytics'),
    path('api/entry_list/', views.APIEntryListView.as_view()),
    path('api/status_list/', views.APIStatusListView.as_view()),
    path('csv/status_list/', views.StatusCSVExportView.as_view()),
]
