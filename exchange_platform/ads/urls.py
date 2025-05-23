from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('create/', views.create_ad, name='create_ad'),
    path('edit/<int:ad_id>/', views.edit_ad, name='edit_ad'),
    path('delete/<int:ad_id>/', views.delete_ad, name='delete_ad'),
    path('', views.ad_list, name='ad_list'),
    path('exchange/<int:ad_id>/', views.create_exchange_proposal, name='create_exchange_proposal'),
    path('proposals/', views.exchange_proposals, name='exchange_proposals'),
    path('update_proposal/<int:proposal_id>/', views.update_exchange_proposal, name='update_exchange_proposal'),
]