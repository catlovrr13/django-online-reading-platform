from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.conf import settings
from .models import Book, Chapter
from .ollama_extractor import OllamaExtractor
from .pollinations_generator import PollinationsGenerator

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0
    fields = ['chapter_number', 'title', 'summary', 'illustration_preview']
    readonly_fields = ['illustration_preview']
    ordering = ['chapter_number']
    
    def illustration_preview(self, obj):
        if obj.illustration:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 5px;" />',
                obj.illustration.url
            )
        return "No image"
    illustration_preview.short_description = 'Preview'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = [
        'cover_preview_small',
        'title', 
        'author',
        'genre',
        'accessibility',
        'status_badge',
        'image_status_badge',
        'created_at'
    ]
    
    list_filter = [
        'accessibility',
        'genre',
        'is_processed',
        'images_generated',
        'language',
        'created_at'
    ]
    
    search_fields = ['title', 'author', 'description']
    
    readonly_fields = [
        'is_processed',
        'images_generated',
        'processing_error',
        'created_at',
        'updated_at',
        'cover_preview_large',
        'cover_prompt',
        'chapter_count'
    ]
    
    inlines = [ChapterInline]
    
    fieldsets = (
        ('Upload Book File', {
            'fields': ('file',),
            'description': 'Upload PDF or EPUB. AI will automatically extract metadata and generate images'
        }),
        ('AI-Generated Cover', {
            'fields': ('cover_preview_large', 'cover_image', 'cover_prompt'),
            'description': 'Cover image generated'
        }),
        ('Book Information', {
            'fields': ('title', 'author', 'genre', 'description', 'language', 'accessibility'),
            'description': 'Metadata extracted'
        }),
        ('Processing Information', {
            'fields': (
                'is_processed',
                'images_generated',
                'processing_error',
                'chapter_count',
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['regenerate_images', 'reprocess_metadata']
    
    def cover_preview_small(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" width="40" height="60" style="object-fit: cover; border-radius: 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.cover_image.url
            )
        return "Cover Image"
    cover_preview_small.short_description = 'Cover'
    
    def cover_preview_large(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 450px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" />',
                obj.cover_image.url
            )
        return "No cover generated yet"
    cover_preview_large.short_description = 'Cover Preview'
    
    def chapter_count(self, obj):
        count = obj.chapters.count()
        return f"{count} chapter{'s' if count != 1 else ''}"
    chapter_count.short_description = 'Total Chapters'
    
    def status_badge(self, obj):
        if obj.is_processed:
            return "Processed"
        elif obj.processing_error:
            return "Error"
        else:
            return "Pending"
    status_badge.short_description = 'Metadata'
    
    def image_status_badge(self, obj):
        if obj.images_generated:
            return "AI Images"
        else:
            return "No Images"
    image_status_badge.short_description = 'Images'
    
    def save_model(self, request, obj, form, change):
        should_process = not change or 'file' in form.changed_data
        
        if should_process:
            super().save_model(request, obj, form, change)
            
            try:
                self.message_user(
                    request,
                    "Step 1/2: Extracting metadata with Ollama AI",
                    level=messages.INFO
                )
                
                extractor = OllamaExtractor()
                result = extractor.process_book(obj.file.path, extract_summaries=True)
                
                obj.title = result['title']
                obj.author = result['author']
                obj.genre = self._normalize_genre(result['genre'])
                obj.description = result['description']
                obj.language = result['language']
                obj.is_processed = True
                obj.processing_error = None
                obj.save()
                
                obj.chapters.all().delete()
                
                chapter_summaries = result.get('chapter_summaries', {})
                for idx, chapter_title in enumerate(result['chapters'], start=1):
                    Chapter.objects.create(
                        book=obj,
                        title=chapter_title,
                        chapter_number=idx,
                        summary=chapter_summaries.get(idx, '')
                    )
                
                self.message_user(
                    request,
                    f"Metadata extracted! Title: '{result['title']}' by {result['author']} "
                    f"({len(result['chapters'])} chapters found)",
                    level=messages.SUCCESS
                )
                
                if getattr(settings, 'GENERATE_BOOK_IMAGES', True):
                    self._generate_free_images(request, obj, result)
                
            except Exception as e:
                obj.is_processed = False
                obj.processing_error = str(e)
                obj.save()
                
                error_msg = str(e)
                if "Ollama not running" in error_msg or "Cannot connect to Ollama" in error_msg:
                    self.message_user(
                        request,
                        "Ollama is not running! Start it with: ollama serve",
                        level=messages.ERROR
                    )
                else:
                    self.message_user(
                        request,
                        f"Processing error: {error_msg}",
                        level=messages.ERROR
                    )
        else:
            super().save_model(request, obj, form, change)
    
    def _generate_free_images(self, request, book_obj, metadata):
        
        try:
            self.message_user(
                request,
                "Step 2/2: Generating images with Pollinations.ai",
                level=messages.INFO
            )
            
            image_gen = PollinationsGenerator()
            
            self.message_user(request, "Generating book cover", level=messages.INFO)
            
            cover_data = {
                'title': metadata['title'],
                'author': metadata['author'],
                'genre': metadata['genre'],
                'description': metadata['description']
            }
            
            cover_file, cover_prompt = image_gen.generate_book_cover(cover_data)
            
            if cover_file:
                book_obj.cover_image.save(
                    f"cover_{book_obj.id}.jpg",
                    cover_file,
                    save=False
                )
                book_obj.cover_prompt = cover_prompt
                self.message_user(
                    request,
                    "Book cover generated",
                    level=messages.SUCCESS
                )
            else:
                self.message_user(
                    request,
                    "Could not generate cover image",
                    level=messages.WARNING
                )
            
            max_images = getattr(settings, 'MAX_CHAPTER_IMAGES', 10)
            chapters = book_obj.chapters.all()[:max_images]
            
            if chapters:
                self.message_user(
                    request,
                    f"Generating {len(chapters)} chapter illustrations...",
                    level=messages.INFO
                )
            
            book_context = {
                'title': metadata['title'],
                'genre': metadata['genre']
            }
            
            generated_count = 0
            for chapter in chapters:
                chapter_data = {
                    'chapter_number': chapter.chapter_number,
                    'title': chapter.title,
                    'summary': chapter.summary
                }
                
                illustration_file, illustration_prompt = image_gen.generate_chapter_illustration(
                    chapter_data,
                    book_context
                )
                
                if illustration_file:
                    chapter.illustration.save(
                        f"chapter_{book_obj.id}_{chapter.chapter_number}.jpg",
                        illustration_file,
                        save=False
                    )
                    chapter.illustration_prompt = illustration_prompt
                    chapter.save()
                    generated_count += 1
            
            book_obj.images_generated = True
            book_obj.save()
            
            self.message_user(
                request,
                f"Generated {generated_count} chapter illustration(s)",
                level=messages.SUCCESS
            )
            
        except Exception as e:
            self.message_user(
                request,
                f"⚠️ Image generation error: {str(e)}",
                level=messages.WARNING
            )
    
    def regenerate_images(self, request, queryset):
        for book in queryset:
            if book.is_processed:
                metadata = {
                    'title': book.title,
                    'author': book.author,
                    'genre': book.genre,
                    'description': book.description
                }
                self._generate_free_images(request, book, metadata)
        
        self.message_user(
            request,
            f"Regenerated images for {queryset.count()} book(s)",
            level=messages.SUCCESS
        )
    regenerate_images.short_description = "Regenerate AI images for selected books"
    
    def reprocess_metadata(self, request, queryset):
        for book in queryset:
            try:
                extractor = OllamaExtractor()
                result = extractor.process_book(book.file.path, extract_summaries=False)
                
                book.title = result['title']
                book.author = result['author']
                book.genre = self._normalize_genre(result['genre'])
                book.description = result['description']
                book.is_processed = True
                book.save()
                
            except Exception as e:
                self.message_user(
                    request,
                    f"Error reprocessing '{book.title}': {e}",
                    level=messages.ERROR
                )
        
        self.message_user(
            request,
            f"Reprocessed metadata for {queryset.count()} book(s)",
            level=messages.SUCCESS
        )
    reprocess_metadata.short_description = "Reprocess metadata for selected books"

    def _normalize_genre(self, ai_genre: str) -> str:
        genre_lower = ai_genre.lower()
        
        genre_map = {
            'fiction': 'fiction',
            'literary fiction': 'fiction',
            'non-fiction': 'non_fiction',
            'nonfiction': 'non_fiction',
            'mystery': 'mystery',
            'detective': 'mystery',
            'science fiction': 'science_fiction',
            'sci-fi': 'science_fiction',
            'scifi': 'science_fiction',
            'fantasy': 'fantasy',
            'romance': 'romance',
            'thriller': 'thriller',
            'suspense': 'thriller',
            'biography': 'biography',
            'autobiography': 'biography',
            'memoir': 'biography',
            'self-help': 'self_help',
            'self help': 'self_help',
            'history': 'history',
            'historical': 'history',
        }
        
        for keyword, genre_value in genre_map.items():
            if keyword in genre_lower:
                return genre_value
        
        return 'other'

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    
    list_display = [
        'book',
        'chapter_number',
        'title',
        'has_illustration',
        'has_summary'
    ]
    
    list_filter = ['book']
    search_fields = ['title', 'book__title', 'summary']
    readonly_fields = ['illustration_preview_large', 'illustration_prompt']
    ordering = ['book', 'chapter_number']
    
    fieldsets = (
        ('Chapter Information', {
            'fields': ('book', 'chapter_number', 'title', 'summary')
        }),
        ('AI-Generated Illustration', {
            'fields': ('illustration_preview_large', 'illustration', 'illustration_prompt'),
            'description': 'Illustration generated'
        }),
    )
    
    def has_illustration(self, obj):
        if obj.illustration:
            return "Yes"
        return "No"
    has_illustration.short_description = 'Has Image'
    
    def has_summary(self, obj):
        if obj.summary:
            return "Yes"
        return "No"
    has_summary.short_description = 'Has Summary'
    
    def illustration_preview_large(self, obj):
        if obj.illustration:
            return format_html(
                '<img src="{}" style="max-width: 600px; max-height: 600px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);" />',
                obj.illustration.url
            )
        return "No illustration generated yet"
    illustration_preview_large.short_description = 'Illustration Preview'