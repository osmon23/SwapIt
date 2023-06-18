from django.urls import path

from .views import SendMessageView

app_name = 'chat'

urlpatterns = [
    path('send-message/', SendMessageView.as_view(), name='send-message'),
]