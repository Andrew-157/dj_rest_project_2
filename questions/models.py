from django.db import models
from django.template.defaultfilters import slugify
from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField(max_length=80)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Question(models.Model):
    title = models.CharField(max_length=155)
    slug = models.SlugField(max_length=200)
    details = models.TextField(null=True)
    author = models.ForeignKey(
        CustomUser, related_name='questions', on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='questions')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
    author = models.ForeignKey(
        CustomUser, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(
        Question, related_name='answers', on_delete=models.CASCADE)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['id']
