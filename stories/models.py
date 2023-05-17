from django.db import models


class Story(models.Model):
    title = models.CharField(max_length=155)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        'users.CustomUser', related_name='stories', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_date']


class Review(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    story = models.ForeignKey(
        'stories.Story', related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(
        'users.CustomUser', related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_date']
