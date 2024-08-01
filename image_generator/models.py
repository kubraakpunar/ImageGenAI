from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid 
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    original_photo = models.ImageField(upload_to='photos/')
    prompted_photo = models.CharField(max_length=255, null=True, blank=True,editable=False)

    class Meta:
        verbose_name =_('User')
        verbose_name_plural =_('Users')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"