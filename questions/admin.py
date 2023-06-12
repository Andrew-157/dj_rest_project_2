from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from questions.models import Question, Answer, AnswerVote, QuestionComment, Tag


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'author', 'published', 'updated',
        'tag_list', 'answers_count', 'comments_count'
    ]
    list_filter = ['title', 'slug', 'author',
                   'published', 'updated', 'tags']
    search_fields = ['title', 'slug']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).\
            select_related('author').\
            prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def answers_count(self, obj):
        return Answer.objects.filter(question__id=obj.id).count()

    def comments_count(self, obj):
        return QuestionComment.objects.filter(question__id=obj.id).count()


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'author', 'question', 'published', 'updated', 'count_votes'
    ]
    list_filter = ['author', 'question', 'published', 'updated']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).\
            select_related('author', 'question')

    def count_votes(self, obj):
        votes = AnswerVote.objects.filter(answer=obj).all()
        votes_useful = votes.filter(useful=True).count()
        votes_not_useful = votes.filter(useful=False).count()
        return {
            'This answer is useful': votes_useful,
            'This answer is not useful': votes_not_useful
        }


@admin.register(QuestionComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'question', 'published', 'updated']
    list_filter = ['author', 'question', 'published', 'updated']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).\
            select_related('author', 'question')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name', 'slug']
    search_fields = ['name', 'slug']
