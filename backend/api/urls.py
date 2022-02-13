from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes" ),
    path('countries/', views.CountryList.as_view(), name="countries" ),
    path('countries/<str:pk>/', views.CountryDetail.as_view(), name="country" ),
    path('characters/', views.CharacterList.as_view(), name="characters" ),
    path('characters/<str:pk>/', views.CharacterDetail.as_view(), name="character" ),
]
