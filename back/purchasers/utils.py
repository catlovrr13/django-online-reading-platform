from .models import UserProfile, SubscriptionType
def can_access_chapter(user, chapter):
    book = chapter.book

    if not user.is_authenticated:
        return book.accessibility == 'free'

    try:
        profile = UserProfile.objects.select_related('subscription_type').get(user=user)
    except UserProfile.DoesNotExist:
        return book.accessibility == 'free'

    if profile.subscription_type.name == SubscriptionType.PREMIUM:
        return True

    if book.accessibility == 'free':
        return True

    first_two = book.chapters.order_by('chapter_number')[:2]
    return chapter in first_two