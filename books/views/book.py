from books.serializers.book_serializer import BookListSerializer
from common.views.base import BaseModelViewset
from books.services.book_services import BookServices
from rest_framework.decorators import action
from rest_framework.response import Response


class BookModelViewset(BaseModelViewset):
    queryset = BookServices().get_all_books()
    serializer_class = BookListSerializer
    authentication_classes = []

    @action(detail=False, methods=["get"])
    def sample_get_api(self, request):
        return Response({"message": "Sample Get API"})
