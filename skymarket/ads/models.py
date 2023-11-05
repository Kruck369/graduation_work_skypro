from django.conf import settings
from django.db import models


class Ad(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, default='')
    description = models.TextField(max_length=1000, null=False, blank=False, default='')
    price = models.IntegerField(null=False, blank=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ads',
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to='ads/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class Comment(models.Model):
    text = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True,
    )
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
