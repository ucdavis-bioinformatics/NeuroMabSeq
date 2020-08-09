from django.urls import path, include
from django.conf.urls import url  #, patterns
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogout, name='Logout'),
    path('edit_metadata/', views.edit_metadata, name='Edit Metadata'),
    path('add_faq/', views.add_faq, name='Add FAQ'),
    path('edit_faq/<int:pk>/', views.edit_faq, name='Edit FAQ'),
    path('delete_faq/<int:pk>/', views.delete_faq, name='Edit FAQ'),
    path('faq_list/', views.FAQListView, name='Add FAQ'),
    path('', views.main_page, name='main page'),
    url(regex=r'^new_query/$', view=views.TrimmerEntryListView, name='sequence_query'),
    path('status/', views.TrimmerStatusListView, name='status'),
    path('fasta_re/', views.fasta_file_response, name='fasta'),
    path('faq/', views.faq_view, name='faq'),
    path('blat/', views.blat, name='Blat'),
    path('new_entry/<int:pk>/', views.TrimmerEntryDetailView.as_view(), name='sequence_entry'),
    path('new_entry/<int:pk>/<int:pk2>/', views.TrimmerEntryDetailView.as_view(), name='sequence_entry'),
    path('query/', views.SequenceListView, name='sequence_entry'),
    # path('analytics/', views.analytics_view, name='analytics'),
    path('api/entry_list/', views.APIEntryListView.as_view()),
    path('api/status_list/', views.APIStatusListView.as_view()),
    path('csv/status_list/', views.StatusCSVExportView.as_view()),
    path('accounts/profile/', views.main_page, name='Main Page'),

]
