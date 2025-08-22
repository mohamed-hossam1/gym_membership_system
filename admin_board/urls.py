from django.urls import path
from . import views


urlpatterns = [
    path('admin-dashboard/',views.admin_dashboard,name='admin-dashboard'),
    path('add-member/', views.add_member, name='add-member'),
    path('scan-qr/', views.scan_qr, name='scan-qr'),
    path('edit-member/<str:unique_id>/', views.edit_member, name='edit-member'),
    path('login/', views.login_view, name='login'),
    path('',views.index, name="index")
]

