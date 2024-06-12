from django.urls import path
from .views import home, send_message, manage_contacts, add_contact, edit_contact, delete_contact

urlpatterns = [
    path('', home, name='home'),
    path('send_message/', send_message, name='send_message'),
    path('manage_contacts/', manage_contacts, name='manage_contacts'),
    path('add_contact/', add_contact, name='add_contact'),
    path('edit_contact/<int:pk>/', edit_contact, name='edit_contact'),
    path('delete_contact/<int:pk>/', delete_contact, name='delete_contact'),
]
