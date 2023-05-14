from django.urls import path
from . import views
app_name = "prediction_urls"
urlpatterns = [
    path('predict/',view=views.Predicition.as_view()),
    path('register/',view=views.RegistrationView.as_view()),
    path('login/',view=views.LoginView.as_view()),
    path('decode/',view=views.DecodeToke.as_view()),
]
