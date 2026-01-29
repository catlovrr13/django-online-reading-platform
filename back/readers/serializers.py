from rest_framework import serializers
from .models import Book, Chapter, BookRating

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'genre',
            'description',
            'cover_image',
            'accessibility',
            'language',
            'average_rating',
            'rating_count'
        ]
        
class ChapterSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(source='book.id', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Chapter
        fields = [
            'id',
            'book_id',
            'book_title',
            'chapter_number',
            'title',
            'summary',
            'illustration'
        ]

#Booking Rating Serializer - Pozon
class BookRatingSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(source='book.id', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = BookRating
        fields = [
            'id',
            'book_id',
            'book_title',
            'user_username',
            'rating',
            'review'
        ]