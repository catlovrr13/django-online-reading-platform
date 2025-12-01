from rest_framework import serializers
from .models import Book, Chapter

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
            'language'
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