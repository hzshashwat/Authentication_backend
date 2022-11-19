from django.urls import path, include
from catalog.views import *


urlpatterns = [
    path('books/', HelloApiView.as_view(), name= 'deletebooks'),
    path('books/find_books_needed/', NeededBooksView, name= 'neededbooks'),
    path('books/unavailable_books/', UnavailableBooksView, name= 'unavailablebooks'),
    path('book/', BookApiView.as_view(), name= 'bookview'),
    path('book/issue_book/', IssueBookApiView.as_view(), name= 'issuebook')
]