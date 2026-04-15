from django.urls import path
from .views import CaptureHoldView, CreateHoldView, ReleaseHoldView

app_name = 'holds'

urlpatterns = [
    path("", CreateHoldView.as_view(), name="create"),
    path("<int:hold_id>/release/", ReleaseHoldView.as_view(), name="release"),
    path("<int:hold_id>/capture/", CaptureHoldView.as_view(), name="capture"),
]