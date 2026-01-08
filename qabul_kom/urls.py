from django.urls import path
from . import views
from news.views import PostListView, post_detail, index
from Abituriyent.views import PrivilegeListView, qabul_kvotasi
from xorijiy.views import home2, application_form, check_status, application_success
from employees.views import KomissiyaView

urlpatterns = [
    # HOME
    path('', index, name='home'),

    # STATIK SAHIFALAR
    path("meyor/", views.RegulatoryDocumentsView.as_view(), name='meyor'),
    path("qabul/", views.qabul_kunlari, name='qabul'),
    path('qabul_kvotasi/', qabul_kvotasi, name='qabul_kvotasi'),
    path('komissiya/', KomissiyaView.as_view(), name='komissiya'),
    path('privileges/', PrivilegeListView.as_view(), name='privileges'),
    path('hujjatlar/', views.hujjatlar, name='hujjatlar'),

    # XORIJIY TALABALAR
    path('xorij/', home2, name='home2'),
    path('apply/', application_form, name='application_form'),
    path('check-status/', check_status, name='check_status'),
    path('success/<int:application_id>/', application_success, name='application_success'),

    # YANGILIKLAR
    path('yangiliklar/', PostListView.as_view(), name='post_list'),
    path('category/<slug:category_slug>/', PostListView.as_view(), name='post_list_by_category'),

    # HUJJATLAR
    path('documents/download/<int:pk>/', views.download_document, name='download_document'),
    path('documents/view/<int:pk>/', views.view_document, name='view_document'),

    # API
    path('api/documents/category/', views.get_documents_by_category, name='documents_by_category'),
    path('api/download/increment/', views.increment_download_count, name='increment_download'),
    path('api/admission/info/', views.get_admission_info, name='admission_info'),

    # ❗ ENG OXIRIDA ❗
    path('<slug:slug>/', post_detail, name='post_detail'),
]
