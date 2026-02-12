from rest_framework import serializers
from .models import Book, Chapter, BookRating, History, Library

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
        
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'progress', 'last_read_at', 'book']
        read_only_fields = ['id', 'last_read_at', 'book']   
        extra_kwargs = {'progress': {'required': False}}
        
class BookInLibrarySerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'description', 'language', 'accessibility', 'cover_url', 'created_at']

    def get_cover_url(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None


class LibrarySerializer(serializers.ModelSerializer):
    books = BookInLibrarySerializer(many=True, read_only=True)

    class Meta:
        model = Library
        fields = ['id', 'books']

# class LibrarySerializer(serializers.ModelSerializer):
#     title = serializers.CharField(source='book.title')
#     author = serializers.CharField(source='book.author')
#     cover_url = serializers.SerializerMethodField()

#     class Meta:
#         model = Library
#         fields = ['id', 'book', 'title', 'author', 'cover_url', 'added_at']

#     def get_cover_url(self, obj):
#         if obj.book.cover:
#             return obj.book.cover.url
#         return None
    
# class GenreSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
    
#     class Meta:
#         model = Genre
#         fields = ['id', 'name']