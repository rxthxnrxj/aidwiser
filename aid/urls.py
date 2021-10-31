from django.urls import path
from .import views
urlpatterns = [
    path('', views.user, name="user"),
    path('ambulance/', views.ambulance, name="ambulance"),
    path('ambulance/<str:pk>/', views.spec_ambulance, name="spec_ambulance"),
    path('hospital/', views.hospital, name="hospital"),
    path('hospital/<str:pk>/', views.spec_hospital, name="spec_hospital"),
    path('driver/', views.driver, name="driver"),
    path('doctor/', views.doctor, name="doctor"),
    path('doctor/<str:pk>/', views.spec_doctor, name="spec_doctor"),
    path('login/', views.login, name="login"),
    path('create_aid/', views.create_aid, name="create_aid")
]
