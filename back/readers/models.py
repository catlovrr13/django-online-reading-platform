from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator


# Create your models here.
class Genre(models.Model):
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
    
    genre = models.CharField(choices=GENRE_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_genre_display()
    

class Book(models.Model):
    ACCESSIBILITY_CHOICES = [
    ('free', 'Free'),
    ('premium', 'Premium'),
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
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, default='English')
    
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
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
    
    # properties for rating - pozon
    @property
    def average_rating(self) -> float | None:
        agg = self.ratings.aggregate(avg=models.Avg('rating'))
        return round(agg['avg'], 1) if agg['avg'] is not None else None

    @property
    def rating_count(self) -> int:
        return self.ratings.count()
    
    class Meta:
        ordering = ['-created_at']
    
class Library(models.Model):
    user = models.OneToOneField(
        'purchasers.UserProfile',
        on_delete=models.CASCADE,
        related_name='library'
    )
    books = models.ManyToManyField(
        Book,
        related_name='in_libraries',
        blank=True
    )
    
    class Meta:
        verbose_name = 'Library'
        verbose_name_plural = 'Libraries'
    
    def __str__(self):
        return f"{self.user.user.username}'s Library"

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
    
# Added Book Ratings function - Pozon
class BookRating(models.Model):          
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        'purchasers.UserProfile',
        on_delete=models.CASCADE,
        related_name='book_ratings'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['book', 'user']
    
    def __str__(self):
        return f"{self.user.user.username} - {self.book.title}: {self.rating}★"

class History(models.Model):
    user = models.ForeignKey(
        'purchasers.UserProfile',
        on_delete=models.CASCADE,
        related_name='reading_history'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='read_by'
    )
    last_read_at = models.DateTimeField(auto_now=True)
    progress = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Reading progress as a percentage"
    )
    
    class Meta:
        unique_together = ['user', 'book']
        ordering = ['-last_read_at']
        verbose_name = 'History'
        verbose_name_plural = 'Histories'
    
    def __str__(self):
        return f"{self.user.user.username} - {self.book.title}: {self.progress}%"