from rest_framework.pagination import PageNumberPagination
from django_filters import FilterSet, CharFilter, ChoiceFilter, NumberFilter
from .models import Book


# PAGINATION CLASSES
class BookPageNumberPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class ChapterPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class RatingPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


# FILTER CLASSES
class BookFilterSet(FilterSet):
    """
    Custom filter for Book model with genre, accessibility, rating range, and language filters.
    
    Usage:
    - /books/?genre=fiction
    - /books/?accessibility=free
    - /books/?min_rating=3.5
    - /books/?language=English
    - /books/?is_processed=true
    """
    genre = CharFilter(field_name='genre__genre', lookup_expr='iexact')
    accessibility = ChoiceFilter(
        choices=Book.ACCESSIBILITY_CHOICES,
        field_name='accessibility'
    )
    min_rating = NumberFilter(
        field_name='ratings__rating',
        lookup_expr='gte',
        method='filter_min_rating'
    )
    language = CharFilter(field_name='language', lookup_expr='iexact')
    is_processed = ChoiceFilter(
        choices=[(True, 'Yes'), (False, 'No')],
        field_name='is_processed'
    )
    
    def filter_min_rating(self, queryset, name, value):
        """Filter books with average rating >= value"""
        from django.db.models import Avg, Q
        return queryset.annotate(
            avg_rating=Avg('ratings__rating')
        ).filter(Q(avg_rating__gte=value) | Q(ratings__isnull=True))
    
    class Meta:
        model = Book
        fields = ['genre', 'accessibility', 'language', 'is_processed']