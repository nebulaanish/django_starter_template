from books.models.book import Book


class BookServices:
    def __init__(self):
        pass

    def get_all_books(self):
        return Book.objects.all()

    def get_book_by_id(self, id):
        return Book.objects.get(id=id)
