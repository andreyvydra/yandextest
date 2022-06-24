from django.urls import path

from restapi import views

urlpatterns = [
    path('nodes/<str:uuid>', views.OfferAndCategoryView.as_view(), name='nodes'),
    path('delete/<str:uuid>', views.OfferAndCategoryDelete.as_view(), name='delete'),
    path('imports', views.OfferAndCategoryImports.as_view(), name='import'),
    path('sales', views.LatestOfferAndCategoryView.as_view(), name='sales')
]
