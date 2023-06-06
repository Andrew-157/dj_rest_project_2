from django.db import models
from django.template.defaultfilters import slugify
from users.models import CustomUser


class Question(models.Model):
    title = models.CharField(max_length=155)
    slug = models.SlugField(max_length=200)
    details = models.TextField(null=True)
    author = models.ForeignKey(
        CustomUser, related_name='questions', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)
