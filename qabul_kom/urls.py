from django.urls import path
from . import views
from news.views import PostListView, post_detail
from news.views import index
from employees.views import KomissiyaView


urlpatterns = [
    path('', index, name='home'),
    path("about/", views.about, name='about'),
    path("meyor/", views.RegulatoryDocumentsView.as_view(), name='meyor'),
    path("documents/download/<int:pk>/", views.download_document, name='download_document'),
    path("documents/view/<int:pk>/", views.view_document, name='view_document'),
    path("qabul/", views.qabul_kunlari, name='qabul'),

    path('komissiya/', KomissiyaView.as_view(), name='komissiya'),
    
    path('yangiliklar/', PostListView.as_view(), name='post_list'),
    path('category/<slug:category_slug>/', PostListView.as_view(), name='post_list_by_category'),
    path('<slug:slug>/', post_detail, name='post_detail'),




    # Hujjatlar ro'yxati
    path('hujjatlar/', views.DocumentListView.as_view(), name='document_list'),
    path('hujjatlar/<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    
    # Fayllar bilan ishlash
    path('download/<int:pk>/', views.download_document, name='download_document'),
    path('view/<int:pk>/', views.view_document, name='view_document'),
    
    # API endpoints
    path('api/documents/category/', views.get_documents_by_category, name='documents_by_category'),
    path('api/download/increment/', views.increment_download_count, name='increment_download'),
    path('api/admission/info/', views.get_admission_info, name='admission_info'),
]