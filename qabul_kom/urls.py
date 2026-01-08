from django.urls import path
from . import views
from magister.views import hujjatlar_t,  Qabul_Rijasi, Magistratura_Natijalari
from news.views import PostListView, post_detail, index
from Abituriyent.views import PrivilegeListView, qabul_kvotasi
from employees.views import KomissiyaView
from xorijiy.views import foreign_student_request, bakalaver, magistr, shartnoma, kontrakt

urlpatterns = [
    # HOME
    path('', index, name='home'),

    # STATIK SAHIFALAR
    path("meyor/", views.RegulatoryDocumentsView.as_view(), name='meyor'),
    path("qabul/", views.qabul_kunlari, name='qabul'),
    path('hujjatlar_t/', hujjatlar_t, name='hujjatlar_t'),
    path('qabul_kvotasi/', qabul_kvotasi, name='qabul_kvotasi'),
    path('qabul-rejasi/', Qabul_Rijasi, name='Qabul_Rijasi'),
    path('natijalar/', Magistratura_Natijalari, name='Magistratura_Natijalari'),
    path('bakalaver/', bakalaver, name='bakalaver'),
    path('magistr/', magistr, name='magistr'),
    path('shartnoma/', shartnoma, name='shartnoma'),
    path('kontrakt/', kontrakt, name='kontrakt'),
    path('komissiya/', KomissiyaView.as_view(), name='komissiya'),
    path('privileges/', PrivilegeListView.as_view(), name='privileges'),
    path('hujjatlar/', views.hujjatlar, name='hujjatlar'),

    # XORIJIY TALABALAR
    path('foreign/', foreign_student_request, name='foreign_request'),


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

    path('<slug:slug>/', post_detail, name='post_detail'),
]
