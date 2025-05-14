from django.urls import path
from .views import TransportSolverView

urlpatterns = [
    path("solve/", TransportSolverView.as_view(), name="solve-transport")
]
