from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Book(models.Model):
    ACCESSIBILITY_CHOICES = [
    ('free', 'Free'),
    ('premium', 'Premium'),
    ]
    
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('mystery', 'Mystery'),
        ('science_fiction', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
        ('biography', 'Biography'),
        ('self_help', 'Self-Help'),
        ('history', 'History'),
        ('other', 'Other'),
    ]
    
    file = models.FileField(
        upload_to='readers/files/',
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'epub']
        )],
        help_text="Upload PDF or EPUB file"
    )
    
    title = models.CharField(max_length=300, blank=True)
    author = models.CharField(max_length=200, blank=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, blank=True)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, default='English')
    
    accessibility = models.CharField(max_length=20, choices=ACCESSIBILITY_CHOICES, default='premium')
    
    cover_image = models.ImageField(
        upload_to='readers/covers/',
        blank=True,
        null=True,
        help_text="AI-generated book cover"
    )
    cover_prompt = models.TextField(blank=True)
    
    is_processed = models.BooleanField(default=False)
    images_generated = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title or f"Book {self.id}"
    
    class Meta:
        ordering = ['-created_at']
    
class Chapter(models.Model):
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='chapters'
    )
    
    title = models.CharField(max_length=300)
    chapter_number = models.PositiveIntegerField()
    summary = models.TextField(blank=True)
    
    illustration = models.ImageField(
        upload_to='readers/chapters/', blank=True, null=True, help_text="AI-generated chapter illustration"
    )
    illustration_prompt = models.TextField(blank=True)
    
    class Meta:
        ordering = ['chapter_number']
        unique_together = ['book', 'chapter_number']
    
    def __str__(self):
        return f"Ch. {self.chapter_number}: {self.title}"