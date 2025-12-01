"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from readers.views import *
from purchasers.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    
    path('books/', BookListView.as_view()),
    
    path('books/<int:pk>/', BookDetailView.as_view()),

    path('api/book/<int:book_id>/chapter/<int:chapter_id>/', ChapterDetailView.as_view(), name='chapter-detail'),
    
    path('api/book/<int:book_id>/chapters/', AllChaptersView.as_view(), name='all-chapters'),
    
    path('api/subscribe/', SubscribeToPremiumView.as_view(), name='subscribe-to-premium'),
    
    path('api/unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
    
    path('subscription-types/', SubscriptionTypeListView.as_view(), name='subscription-type-list-create'),
    
    path('subscription-types/<int:pk>/', SubscriptionTypeDetailView.as_view(), name='subscription-type-detail'),
    
    path('api/user-profiles/', UserProfileListView.as_view(), name='user-profile-list-create'),
    
    path('api/user-profiles/<int:pk>/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
