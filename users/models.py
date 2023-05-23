from django.db import models
from django.contrib.auth.models import AbstractUser
from users.validators import validate_file_size


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='users/images',
                              validators=[validate_file_size])

    class Meta:
        ordering = ['id']
