from django.shortcuts import render
from .serializers import *
from .models import Book, Chapter
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import CanAccessChapter
from rest_framework.exceptions import NotFound

# Create your views here.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'author__name', 'genre__name', 'accessibility']
    
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ChapterDetailView(generics.RetrieveAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [CanAccessChapter]
    
    def get_object(self):
        book_id = self.kwargs['book_id']
        chapter_number = self.kwargs['chapter_id']

        try:
            chapter = Chapter.objects.select_related('book').get(
                chapter_number=chapter_number,
                book_id=book_id
            )
        except Chapter.DoesNotExist:
            raise NotFound("Chapter not found in this book.")
        
        self.check_object_permissions(self.request, chapter)
        
        return chapter
    
class AllChaptersView(generics.ListAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated, CanAccessChapter]
    
    def get_queryset(self):
        book_id = self.kwargs['book_id']
        chapters = Chapter.objects.filter(book_id=book_id).select_related('book')
        
        accessible_chapters = [
            chapter for chapter in chapters
            if CanAccessChapter().has_object_permission(self.request, self, chapter)
        ]
        
        return accessible_chapters