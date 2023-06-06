# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers
# from questions import views

# router = DefaultRouter()
# router.register(r'questions', views.QuestionViewSet, basename='question')

# questions_router = routers.NestedSimpleRouter(
#     router, r'questions', lookup='question'
# )
# questions_router.register(
#     r'answers', views.AnswerViewSet, basename='question-answer'
# )

# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(questions_router.urls))
# ]
