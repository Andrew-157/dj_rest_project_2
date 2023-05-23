from django.db import models


class Story(models.Model):
    title = models.CharField(max_length=155)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        'users.CustomUser', related_name='stories', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Review(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    story = models.ForeignKey(
        'stories.Story', related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(
        'users.CustomUser', related_name='reviews', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_date']


class Rating(models.Model):
    rating_choices = [(0, 0), (1, 1), (2, 2),
                      (3, 3), (4, 4), (5, 5),
                      (6, 6), (7, 7), (8, 8),
                      (9, 9), (10, 10)]
    author = models.ForeignKey('users.CustomUser',
                               related_name='ratings', on_delete=models.CASCADE)
    story = models.ForeignKey('stories.Story', on_delete=models.CASCADE,
                              related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=rating_choices)
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pub_date']
