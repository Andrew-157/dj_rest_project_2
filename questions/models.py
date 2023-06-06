# from django.db import models
# from users.models import CustomUser


# class Question(models.Model):
#     content = models.TextField()
#     author = models.ForeignKey(
#         CustomUser, related_name='questions', on_delete=models.CASCADE)
#     published = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['id']


# class Answer(models.Model):
#     question = models.ForeignKey(
#         Question, on_delete=models.CASCADE, related_name='answers')
#     author = models.ForeignKey(
#         CustomUser, on_delete=models.CASCADE
#     )
#     content = models.TextField()
#     published = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['id']


# class AnswerStatus(models.Model):
#     STATUS_CHOICES = [
#         ('Useless', 'Useless'),
#         ('Useful', 'Useful')
#     ]
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     status = models.CharField(choices=STATUS_CHOICES, max_length=10)
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#     class Meta:
#         ordering = ['id']


# class QuestionComment(models.Model):
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     question = models.ForeignKey(
#         Question, on_delete=models.CASCADE, related_name='comments')
#     content = models.TextField()

#     class Meta:
#         ordering = ['id']


# class AnswerComment(models.Model):
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     answer = models.ForeignKey(
#         Answer, on_delete=models.CASCADE, related_name='comments'
#     )
#     content = models.TextField()

#     class Meta:
#         ordering = ['id']
