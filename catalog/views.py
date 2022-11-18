from django.shortcuts import render
from .serializer import BookSerializers, ChangeRecordSerializer, UpdateRecordSerializers
from catalog.models import Book
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from catalog.permissions import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.views import APIView
import uuid


# Create your views here.
class HelloApiView(APIView):
    serializer_class = BookSerializers
    authentication_classes = (TokenAuthentication, )
    permission_classes = (
            IsAuthenticatedOrReadOnly,
        )

    def get(self, request, format = None):
        book = Book.objects.all()
        try:
            bookjson = BookSerializers(book, many=True)
            return Response({"message" : [bookjson.data]})
        except Exception as e:
            return Response({"error": str(e)})

    def post(self, request):
        try :
            bookdata = request.data
            bookobj = BookSerializers(data = bookdata)
            if bookobj.is_valid() == True:
                bookobj.validated_data['name'] = self.request.user
                bookobj.validated_data['book_issue_id'] = uuid.uuid4()
                bookobj.save()
                return Response({"message": "Your data is saved successfully",
                "status": "Success"
                })
            else :
                return Response({"message": bookobj.errors,
                "status": "Failed"
                })
        except Exception as e:
            return Response({"message": str(e)})

    def delete(self, request):
        permission_classes = (
            IsAdminUser,
        )
        try:
            book = Book.objects.all().delete()
            return Response({"message" : "All the book records have been deleted successfully."})
        except Exception as e:
            return Response({"error": str(e)})

@api_view(['GET'])
def NeededBooksView(request):
    if request.method == 'GET' :
        limit = int(request.query_params['n'])
        print(limit)
        book = Book.objects.all().filter(inventory__lt = limit)
        try:
            bookjson = BookSerializers(book, many=True)
            return Response({"message" : [bookjson.data]})
        except Exception as e:
            return Response({"error": str(e)})

@api_view(['GET'])
def UnavailableBooksView(request):
    if request.method == 'GET' :
        book = Book.objects.all().filter(inventory = 0)
        try:   
            bookjson = BookSerializers(book, many=True)
            return Response({"message" : [bookjson.data]})
        except Exception as e:
            return Response({"error": str(e)})

class BookViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication, ) 
    serializer_class = BookSerializers
    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self):
        user = self.request.user
        book = Book.objects.filter(name = user)
        return book

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(name = self.request.user)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# @permission_classes([IsAdminUser])
# def BookView(request):
#     if request.method == 'GET' :
#         try:
#             book = Book.objects.get(isbn_no = request.query_params['isbn_no'])
#             bookjson = BookSerializers(book, many=False)
#             if bookjson.is_valid() == True:
#                 return Response({"message" : [bookjson.data]})
#             else:
#                 return Response({"message": bookjson.errors,
#                 "status": "Failed"
#                 })
#         except Exception as e:
#             return Response({"error": str(e)})

#     elif request.method == 'PUT' :
#         book = Book.objects.get(isbn_no = request.query_params['isbn_no'])
#         try :
#             bookobj = ChangeRecordSerializer(book, data=request.data)
#             if bookobj.is_valid():
#                 bookobj.save()
#                 return Response({"message" : "Book record replaced successfully."})
#             else :
#                 return Response({"message": bookobj.errors,
#                 "status": "Failed"
#                 })
#         except Exception as e:
#             return Response({"message": str(e)})
    
#     elif request.method == 'PATCH' :
#         book = Book.objects.get(isbn_no = request.query_params['isbn_no'])
#         try :
#             bookobj = UpdateRecordSerializers(book, data=request.data)
#             if bookobj.is_valid():
#                 bookobj.save()
#                 return Response({"message" : "Book record updated successfully."})
#             else :
#                 return Response({"message": bookobj.errors,
#                 "status": "Failed"
#                 })
#         except Exception as e:
#             return Response({"message": str(e)})

#     elif request.method == 'DELETE' :
#         try:
#             book = Book.objects.get(isbn_no = request.query_params['isbn_no']).delete()
#             return Response({"message" : "The book record has been deleted successfully."})
#         except Exception as e:
#             return Response({"error": str(e)})

@api_view(['GET'])
def IssueBookView(request) :
    if request.method == 'GET':
        try:
            book = Book.objects.get(isbn_no = request.query_params['isbn_no'])
            book.inventory -= 1
            book.save()
            return Response({"message" : "Book issued successfully and Inventory updated."})
        except Exception as e:
            return Response({"error": str(e)})