from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name='threads', blank=True)
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated', auto_now=True)
    name = models.CharField(max_length=50, verbose_name='Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Thread')
        verbose_name_plural = _('Threads')
        ordering = ('created',)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    text = models.CharField(max_length=500, verbose_name='text')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.created} {self.text}'

    class Meta:
        ordering = ('created',)
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

