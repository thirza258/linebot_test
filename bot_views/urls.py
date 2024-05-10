from django.urls import path
from . import views

urlpatterns = [
    # Add your URL patterns here
    # Example: path('home/', views.home, name='home'),
    path("text_message_user/", views.TextMessageUserViews.as_view()),
]