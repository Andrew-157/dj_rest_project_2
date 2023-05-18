from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from stories import views

router = DefaultRouter()
router.register(r'stories', views.StoryViewSet, basename='story')
router.register(r'authors', views.AuthorViewSet, basename='author')

stories_router = routers.NestedSimpleRouter(
    router, r'stories', lookup='story'
)
stories_router.register(
    r'reviews', views.ReviewsByStoryViewSet, basename='story-review')

authors_router = routers.NestedSimpleRouter(
    router, r'authors', lookup='author'
)
authors_router.register(
    r'reviews', views.ReviewsByAuthorViewSet, basename='author-review'
)
stories_router.register(
    r'ratings', views.RatingViewSet, basename='story-rating'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(stories_router.urls)),
    path('', include(authors_router.urls))
]
