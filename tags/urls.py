from tags import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("tags", views.TagViewSet)

app_name = "tags"

urlpatterns = [
    path("", include(router.urls)),
]
