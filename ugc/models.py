from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='user\'s ID',
        unique=True
    )
    name = models.TextField(
        verbose_name='user\'s name'
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'


class Message(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='profile',
        on_delete=models.PROTECT
    )
    text = models.TextField(
        verbose_name='text'
    )
    created_at = models.DateTimeField(
        verbose_name='datetime of receipt',
        auto_now_add=True
    )

    def __str__(self):
        return f'Message {self.pk} from {self.profile}'

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
