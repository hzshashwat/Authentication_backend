from django.urls import path, include
from catalog.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('book', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    path('books/', HelloApiView.as_view(), name= 'deletebooks'),
    path('books/find_books_needed/', NeededBooksView, name= 'neededbooks'),
    path('books/unavailable_books/', UnavailableBooksView, name= 'unavailablebooks'),
    #path('book/', BookView, name= 'bookview'),
    path('book/issue_book/', IssueBookView, name= 'issuebook')
]