from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed


class Thread(models.Model):
    participant = models.ManyToManyField(User, db_table='User', related_name='User')
    created = models.DateTimeField(verbose_name='created', auto_now=True)
    updated = models.DateTimeField(verbose_name='updated', blank=True, null=True)

    def __str__(self):
        return f'Thread from {self.created} between {self.participant.all()[0].username} and ' \
               f'{self.participant.all()[1].username}'

    class Meta:
        ordering = ('created',)


# to limit the number of users in one thread, we use django signals
def participant_changed(sender, **kwargs):
    if kwargs['instance'].participant.count() > 2:
        raise ValidationError("You can't assign more than two participant")


m2m_changed.connect(participant_changed, sender=Thread.participant.through)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    text = models.CharField(max_length=500, verbose_name='text')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread')
    created = models.DateTimeField(verbose_name='created', auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.created} {self.text}'

    class Meta:
        ordering = ('created',)

# Create your models here.

