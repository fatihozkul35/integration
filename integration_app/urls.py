from django.urls import path
from django.views.i18n import set_language
from . import views

app_name = 'integration_app'

urlpatterns = [
    path('', views.index, name='index'),
    # path('services/', views.services, name='services'),
    path('uber-uns/', views.about, name='about'),
    # path('ablauf/', views.process, name='process'),
    # path('preise/', views.pricing, name='pricing'),
    path('faq/', views.faq, name='faq'),
    path('referenzen/', views.references, name='references'),
    path('blog/', views.blog, name='blog'),
    path('kontakt/', views.contact, name='contact'),
    path('set-language/', set_language, name='set_language'),
]

