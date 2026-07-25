from django.urls import path

from . import views

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("chat/<int:conversation_id>/", views.inbox, name="conversation"),
    path("chat/<int:conversation_id>/send/", views.send_message, name="send_message"),
]
