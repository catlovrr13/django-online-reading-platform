from django.shortcuts import render
from .serializers import *
from .models import Book, Chapter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import CanAccessChapter
from rest_framework.exceptions import NotFound
from .ollama_extractor import OllamaExtractor
from .pollinations_generator import PollinationsGenerator
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import get_object_or_404

# Create your views here.
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    
    def create(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided. Please upload a PDF or EPUB file.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = request.FILES['file']
        
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension not in ['pdf', 'epub']:
            return Response(
                {'error': 'Invalid file type. Only PDF and EPUB files are supported.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        accessibility = request.data.get('accessibility', 'premium')
        if accessibility not in ['free', 'premium']:
            accessibility = 'premium'
            
        try:
            book = Book.objects.create(
                file=uploaded_file,
                accessibility=accessibility,
                is_processed=False,
                images_generated=False
            )
            
            try:
                extractor = OllamaExtractor()
                result = extractor.process_book(book.file.path, extract_summaries=True)
                
                book.title = result['title']
                book.author = result['author']
                book.genre = self._normalize_genre(result['genre'])
                book.description = result['description']
                book.language = result['language']
                book.is_processed = True
                book.save()
                
                chapter_summaries = result.get('chapter_summaries', {})
                for idx, chapter_title in enumerate(result['chapters'], start=1):
                    Chapter.objects.create(
                        book=book,
                        title=chapter_title,
                        chapter_number=idx,
                        summary=chapter_summaries.get(idx, '')
                    )
                
                print(f"Metadata extracted: '{result['title']}' by {result['author']}")
                
            except Exception as e:
                book.processing_error = f"Metadata extraction failed: {str(e)}"
                book.save()
                
                return Response(
                    {
                        'error': 'AI metadata extraction failed',
                        'details': str(e),
                        'book_id': book.id,
                        'message': 'Book uploaded but metadata extraction failed. You can manually edit in admin.'
                    },
                    status=status.HTTP_206_PARTIAL_CONTENT
                )
            
            if getattr(settings, 'GENERATE_BOOK_IMAGES', True):
                try:
                    self._generate_images(book, result)
                except Exception as e:
                    print(f"Image generation failed: {e}")
            
            serializer = self.get_serializer(book)
            
            return Response(
                {
                    'message': 'Book uploaded and processed successfully',
                    'book': serializer.data,
                    'metadata': {
                        'title': book.title,
                        'author': book.author,
                        'genre': book.genre,
                        'chapters_found': book.chapters.count(),
                        'cover_generated': bool(book.cover_image),
                        'illustrations_generated': book.images_generated
                    }
                },
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            return Response(
                {'error': f'Upload failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _generate_images(self, book, metadata):
        """Generate cover and chapter images"""
        image_gen = PollinationsGenerator()
        
        cover_file, cover_prompt = image_gen.generate_book_cover({
            'title': metadata['title'],
            'author': metadata['author'],
            'genre': metadata['genre'],
            'description': metadata['description']
        })
        
        if cover_file:
            book.cover_image.save(f"cover_{book.id}.jpg", cover_file, save=False)
            book.cover_prompt = cover_prompt
        
        max_images = getattr(settings, 'MAX_CHAPTER_IMAGES', 10)
        chapters = book.chapters.all()[:max_images]
        
        generated_count = 0
        for chapter in chapters:
            illustration_file, illustration_prompt = image_gen.generate_chapter_illustration(
                {
                    'chapter_number': chapter.chapter_number,
                    'title': chapter.title,
                    'summary': chapter.summary
                },
                {
                    'title': metadata['title'],
                    'genre': metadata['genre']
                }
            )
            
            if illustration_file:
                chapter.illustration.save(
                    f"chapter_{book.id}_{chapter.chapter_number}.jpg",
                    illustration_file,
                    save=False
                )
                chapter.illustration_prompt = illustration_prompt
                chapter.save()
                generated_count += 1
        
        book.images_generated = True
        book.save()
        
        print(f"Generated cover and {generated_count} chapter illustrations")
    
    def _normalize_genre(self, ai_genre: str) -> str:
        """Map AI genre to model choices"""
        genre_lower = ai_genre.lower()
        
        genre_map = {
            'fiction': 'fiction',
            'non-fiction': 'non_fiction',
            'mystery': 'mystery',
            'science fiction': 'science_fiction',
            'fantasy': 'fantasy',
            'romance': 'romance',
            'thriller': 'thriller',
            'biography': 'biography',
            'self-help': 'self_help',
            'history': 'history',
        }
        
        for keyword, genre_value in genre_map.items():
            if keyword in genre_lower:
                return genre_value
        
        return 'other'
    
class BookUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        book = self.get_object()
        serializer = self.get_serializer(book, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        book.delete()
        return Response(
            {'message': f'Book {book.title} deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )

class ChapterCreateView(generics.CreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        book_id = self.kwargs['book_id']
        book = get_object_or_404(Book, pk=book_id)
        serializer.save(book=book)

class ChapterUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChapterSerializer
    permission_classes = [IsAdminUser]
    lookup_url_kwarg_book = 'book_id'
    lookup_url_kwarg_chapter = 'chapter_number'

    def get_queryset(self):
        book_id = self.kwargs[self.lookup_url_kwarg_book]
        return Chapter.objects.filter(book_id=book_id)

    def get_object(self):
        queryset = self.get_queryset()
        book_id = self.kwargs[self.lookup_url_kwarg_book]
        chapter_number = self.kwargs[self.lookup_url_kwarg_chapter]

        chapter = get_object_or_404(
            queryset,
            book_id=book_id,
            chapter_number=chapter_number
        )
        
        return chapter

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
        queryset = Chapter.objects.filter(book_id=book_id).select_related('book')
        
        return self.filter_queryset(queryset)