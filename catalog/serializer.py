from rest_framework import serializers
from catalog.models import Book

class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {'name' : {'read_only' : True}, 'book_issue_id' : {'read_only' : True}}

class ChangeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'author_name', 'genre', 'inventory', 'book_issue_id', 'book_name']
        extra_kwargs = {'name' : {'read_only' : True}, 'book_issue_id' : {'read_only' : True}}

class UpdateRecordSerializers(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=100, allow_blank=True)
    author_name = serializers.CharField(required=False, max_length=100, allow_blank=True)
    genre = serializers.CharField(required=False, max_length=100, allow_blank=True)
    inventory = serializers.IntegerField(required=False)
    book_name = serializers.CharField(required=False, max_length=100, allow_blank=True)
    class Meta:
        model = Book
        fields = ['name', 'author_name', 'genre', 'inventory', 'book_name']
