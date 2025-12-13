from django.urls import path
from . import views

app_name = 'integration_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('hakkimizda/', views.about, name='about'),
    path('hizmetler/', views.services, name='services'),
    path('kontakt/', views.contact, name='contact'),
    path('hukuki-bilgilendirme/', views.legal_info, name='legal_info'),
    path('vize-yollari/', views.visa_routes, name='visa_routes'),
    path('surec-nasil-isler/', views.process, name='process'),
    path('isverenler-icin/', views.employers, name='employers'),
    path('faq/', views.faq, name='faq'),
    path('referenzen/', views.references, name='references'),
    path('blog/', views.blog, name='blog'),
    path('urls/', views.urls_list, name='urls_list'),
]
