from django.urls import include, path
from rest_framework.routers import DefaultRouter
from books.views.book import BookModelViewset

router = DefaultRouter()
router.register(r"books", BookModelViewset, basename="books")

urlpatterns = [path("", include(router.urls))]
