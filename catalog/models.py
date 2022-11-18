from django.db import models
from django.core.validators import  MaxLengthValidator,  MinLengthValidator, MinValueValidator
from django.conf import settings

# Create your models here.
class Book(models.Model):
    name = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    book_issue_id = models.CharField(max_length=100, primary_key=True, unique=True)
    book_name = models.CharField(max_length=100, default='Not Available')
    isbn_no = models.CharField('ISBN', max_length = 13, validators=[ MaxLengthValidator(13 , message="As per ISBN standard, all ISBNs are 13-digits long."), MinLengthValidator(13, message="As per ISBN standard, all ISBNs are 13-digits long.")])
    author_name = models.CharField(max_length = 150)
    genre = models.CharField(max_length = 100)
    inventory = models.IntegerField(default = 0, validators=[ MinValueValidator(0)])

