from about.apps import AboutConfig

from about.views import AboutAuthorView, AboutTechView

from django.urls import path

app_name = AboutConfig.name

urlpatterns = [
    path('author/', AboutAuthorView.as_view(), name='author'),
    path('tech/', AboutTechView.as_view(), name='tech'),
]
