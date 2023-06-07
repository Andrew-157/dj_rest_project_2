from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from questions import views


router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet, basename='question')
# /questions/
# /questions/{pk}/

questions_router = routers.NestedSimpleRouter(
    router, r'questions', lookup='question'
)


questions_router.register(
    r'answers', views.AnswerViewSet, basename='question-answer'
)
# /questions/{question_pk}/answers/
# /questions/{question_pk}/answers/{pk}

questions_router.register(
    r'comments', views.QuestionCommentViewSet, basename='question-comment'
)
# /questions/{question_pk}/comments/
# /questions/{question_pk}/comments/{pk}

answers_router = routers.NestedSimpleRouter(
    questions_router, r'answers', lookup='answer'
)
answers_router.register(r'votes', views.AnswerVoteViewSet,
                        basename='question-answer-vote')
# /questions/{question_pk}/answers/{answer_pk}/votes/
# /questions/{question_pk}/answers/{answer_pk}/votes/{pk}


urlpatterns = [
    path('', include(router.urls)),
    path('', include(questions_router.urls)),
    path('', include(answers_router.urls))
]
